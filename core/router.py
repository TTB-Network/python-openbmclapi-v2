from core.orm import writeAgent
from core.api import getStatus
from core.storages import AListStorage
from core.logger import logger
from aiohttp import web
from typing import Union
from multidict import MultiMapping
import aiohttp
import base64
import hashlib
import time
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

    def checkSign(self, hash: str, secret: str, query: MultiMapping) -> bool:
        if not (s := query.get("s")) or not (e := query.get("e")):
            return False
        sign = (
            base64.urlsafe_b64encode(
                hashlib.sha1(f"{secret}{hash}{e}".encode()).digest()
            )
            .decode()
            .rstrip("=")
        )
        return sign == s and time.time() < int(e, 36)

    def init(self) -> None:
        @self.route.get("/download/{hash}")
        async def _(
            request: web.Request,
        ) -> Union[web.Response, web.FileResponse]:
            self.connection += 1
            writeAgent(request.headers["User-Agent"], 1)
            file_hash = request.match_info.get("hash", "").lower()
            if not self.checkSign(file_hash, self.secret, request.query):
                return web.Response(text="Invalid signature.", status=403)

            response = await random.choice(self.storages).express(
                file_hash, self.counters
            )

            self.connection -= 1
            logger.debug(response)
            return response

        @self.route.get("/measure/{size}")
        async def _(request: web.Request) -> Union[web.Response, web.StreamResponse]:
            try:
                size = int(request.match_info.get("size", "0"))

                if (
                    not self.checkSign(f"/measure/{size}", self.secret, request.query)
                    or size > 200
                ):
                    return web.HTTPForbidden() if size > 200 else web.HTTPBadRequest()

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

        @self.route.get("/")
        async def _(_: web.Request) -> web.HTTPFound:
            return web.HTTPFound("/dashboard")

        @self.route.get("/dashboard")
        @self.route.get("/dashboard/{tail:.*}")
        async def _(_: web.Request) -> web.FileResponse:
            return web.FileResponse("./assets/dashboard/index.html")

        self.route.static("/", "./assets/dashboard")

        self.app.add_routes(self.route)