from core.orm import writeAgent
from core.config import Config
from core.utils import checkSign
from core.api import getStatus
from core.storages import AListStorage
from core.logger import logger
from aiohttp import web, WSMsgType
import aiohttp
import random


class Router:
    def __init__(self, app: web.Application, cluster) -> None:
        self.app = app
        self.secret = cluster.secret
        self.storages = cluster.storages
        self.counters = {"hits": 0, "bytes": 0}
        self.route = web.RouteTableDef()
        self.cluster = cluster
        self.ws_clients = []
        self.connection = 0

    def init(self) -> None:
        logger.add(self.pushLog, level="DEBUG")
        @self.route.get("/download/{hash}")
        async def _(
            request: web.Request,
        ) -> web.Response:
            self.connection += 1
            writeAgent(request.headers["User-Agent"], 1)
            file_hash = request.match_info.get("hash", "").lower()
            if not checkSign(file_hash, self.secret, request.query):
                return web.Response(text="Invalid signature.", status=403)

            response = await random.choice(self.storages).express(
                file_hash, self.counters
            )

            self.connection -= 1
            logger.debug(response)
            return response

        @self.route.get("/measure/{size}")
        async def _(request: web.Request) -> web.Response:
            try:
                size = int(request.match_info.get("size", "0"))

                if (
                    not checkSign(f"/measure/{size}", self.secret, request.query)
                    or size > 200
                ):
                    return web.Response(status=403 if size > 200 else 400)

                response = None
                for storage in self.storages:
                    if isinstance(storage, AListStorage):
                        url = await storage.measure(size)
                        response = web.HTTPFound(url)
                        return response

                buffer = b"\x00\x66\xcc\xff" * 256 * 1024
                response = web.StreamResponse(
                    status=200,
                    reason="OK",
                    headers={
                        "Content-Length": str(size * 1024 * 1024),
                        "Content-Type": "application/octet-stream",
                    },
                )

                await response.prepare(request)
                for _ in range(size):
                    await response.write(buffer)
                await response.write_eof()
                return response

            except ValueError:
                return web.Response(status=400)

        @self.route.get("/api/status")
        async def _(_: web.Request) -> web.Response:
            return await getStatus(self.cluster)

        @self.route.get("/api/rank")
        async def _(_: web.Request) -> web.Response:
            async with aiohttp.ClientSession("https://bd.bangbang93.com") as session:
                data = await session.get("/openbmclapi/metric/rank")
                response = web.json_response(await data.json())
                return response
        
        @self.route.get("/ws/logs")
        async def _(request: web.Request) -> web.WebSocketResponse:
            ws = web.WebSocketResponse()
            await ws.prepare(request)

            self.ws_clients.append(ws)
            logger.debug("WebSocket client connected.")

            try:
                while True:
                    msg = await ws.receive()
                    if msg.type == WSMsgType.TEXT:
                        pass

            except Exception:
                pass
            finally:
                self.ws_clients.remove(ws)
            return ws

        @self.route.get("/")
        async def _(_: web.Request) -> web.HTTPFound:
            return web.HTTPFound("/dashboard")

        @self.route.get("/dashboard")
        @self.route.get("/dashboard/{tail:.*}")
        async def _(_: web.Request) -> web.FileResponse:
            return web.FileResponse("./assets/dashboard/index.html")

        self.route.static("/", "./assets/dashboard")

        self.app.add_routes(self.route)

    async def pushLog(self, message: str) -> None:
        if self.ws_clients:
            for ws in self.ws_clients:
                try:
                    await ws.send_str(message)
                except Exception:
                    pass