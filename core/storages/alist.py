from core.classes import Storage, FileInfo, FileList
from core.scheduler import scheduler, IntervalTrigger
from core.logger import logger
from core.i18n import locale
from typing import List, Set, Tuple, Dict, Any
from tqdm import tqdm
from aiohttp import web
import aiohttp
import secrets
import io
import asyncio
import humanize


class AListStorage(Storage):
    def __init__(self, username: str, password: str, url: str, path: str) -> None:
        self.username = username
        self.password = password
        self.url = url
        self.path = path
        self.token = ""
        self.scheduler = None
        self.headers = {}

    async def init(self) -> None:
        async def fetchToken() -> None:
            logger.tinfo("storage.info.alist.fetch_token")
            async with aiohttp.ClientSession(self.url) as session:
                try:
                    async with session.post("/api/auth/login", json={"username": self.username, "password": self.password}) as response:
                        response.raise_for_status()
                        data = await response.json()
                        if data["code"] != 200:
                            raise aiohttp.ClientResponseError(status=data["code"], request_info=response.request_info, history=response.history)
                        self.token = data["data"]["token"]
                        self.headers = {"Authorization": self.token}
                    logger.tsuccess("storage.success.alist.fetch_token")
                except Exception as e:
                    logger.terror("storage.error.alist.fetch_token", e=e)
            if not self.scheduler:
                self.scheduler = scheduler.add_job(fetchToken, IntervalTrigger(days=2))

        await fetchToken()

    async def check(self) -> None:
        file_name = secrets.token_hex(8)
        file_path = self.path + file_name
        try:
            async with aiohttp.ClientSession(self.url, headers={**self.headers, "File-Path": file_path, "Content-Type": "application/octet-stream"}) as session:
                response = await session.put("/api/fs/put", data=b"")
                response.raise_for_status()
                data = await response.json()
                if data["code"] != 200:
                    raise aiohttp.ClientResponseError(status=data["code"], request_info=response.request_info, history=response.history)
            async with aiohttp.ClientSession(self.url, headers=self.headers) as session:
                response = await session.post("/api/fs/remove", json={"names": [file_name], "dir": self.path})
                response.raise_for_status()
                data = await response.json()
                if data["code"] != 200:
                    raise aiohttp.ClientResponseError(status=data["code"], request_info=response.request_info, history=response.history)
            logger.tsuccess("storage.success.alist.check")
        except Exception as e:
            logger.terror("storage.error.alist.check", e=e)

    async def getMissingFiles(self, files: FileList, pbar: tqdm) -> FileList:
        existing_files: List[FileInfo] = []
        async with aiohttp.ClientSession(self.url, headers=self.headers) as session:
            async def getFileList(dir: str, pbar: tqdm) -> List[FileInfo]:
                file_path = self.path + dir
                response = await session.post("/api/fs/list", headers=self.headers, json={"path": file_path})
                response.raise_for_status()
                data = await response.json()
                pbar.update(1)
                if data["code"] != 200:
                    return []
                return [FileInfo(size=content["size"], hash=content["name"], path="", mtime=-1) for content in data["data"]["content"] if not content["is_dir"]]
            
            with tqdm(desc=locale.t("storage.tqdm.alist.get_filelist"), total=256) as _pbar:
                for i in range(256):
                    dir = f"/{i:02x}"
                    existing_files += await getFileList(dir, _pbar)

        existing_info: Set[Tuple[str, int]] = {(file.hash, file.size) for file in existing_files}
        missing_files = []
        for file in files.files:
            pbar.update(1)
            if (file.hash, file.size) not in existing_info:
                missing_files.append(file)

        return FileList(files=missing_files)

    async def measure(self, size: int, request: web.Request, response):
        file_path = f"{self.path}/measure/.{size}"
        try:
            async with aiohttp.ClientSession(self.url, headers=self.headers) as session:
                response = await session.post("/api/fs/get", json={"path": file_path, "password": self.password})
                response.raise_for_status()
                data = await response.json()
                logger.debug(data)
                if data["code"] == 200:
                    logger.debug(1)
                    response = web.HTTPFound(data["data"]["raw_url"])
                    response.prepare(request)
                    return

                if data["code"] != 200:
                    logger.debug(2)
                    try:
                        buffer = b"\x00\x66\xcc\xff" * 256 * 1024
                        response = await session.put("/api/fs/put", data=buffer, headers={**self.headers, "File-Path": file_path, "Content-Type": "application/octet-stream"})
                        response.raise_for_status()
                        data = await response.json()
                        if data["code"] != 200:
                            raise aiohttp.ClientResponseError(status=500, request_info=response.request_info, history=response.history)
                    except Exception as e:
                        logger.terror("storage.error.alist.upload", e=e)
                        raise

                response = await session.post("/api/fs/get", json={"path": file_path, "password": self.password})
                response.raise_for_status()
                data = await response.json()
                logger.debug(data)
                logger.debug(3)
                response = web.HTTPFound(data["data"]["raw_url"])
                response.prepare(request)
                return
        except Exception as e:
            logger.terror("storage.error.alist.measure", e=e)
            return

    async def express(self, hash: str, request: web.Request, response) -> Dict[str, Any]:
        path = f"{self.path}/{hash[:2]}/{hash}"
        async with aiohttp.ClientSession(self.url, headers=self.headers) as session:
            res = await session.post("/api/fs/get", json={"path": path, "password": self.password})
            data = await res.json()
            if data["code"] != 200:
                response = web.HTTPNotFound()
                await response.prepare(request)
                return {"bytes": 0, "hits": 0}
            try:
                response = web.HTTPFound(data["raw_url"])
                response.headers["x-bmclapi-hash"] = hash
                await response.prepare(request)
                return {"bytes": data["size"], "hits": 1}
            except Exception as e:
                response = web.HTTPInternalServerError(reason=e)
                await response.prepare(request)
                logger.debug(e)
                return {"bytes": 0, "hits": 0}

    async def writeFile(self, file: FileInfo, content: io.BytesIO, delay: int, retry: int) -> bool:
        file_path = f"{self.path}/{file.hash[:2]}/{file.hash}"
        async def getSize() -> int:
            async with aiohttp.ClientSession(self.url, headers=self.headers) as session:
                response = await session.post("/api/fs/get", json={"path": file_path, "password": self.password})
                response.raise_for_status()
                data = await response.json()
                if data["code"] != 200:
                    raise aiohttp.ClientResponseError(status=data["code"], request_info=response.request_info, history=response.history)
                return data["data"]["size"]

        for _ in range(retry):
            try:
                async with aiohttp.ClientSession(self.url, headers={**self.headers, "File-Path": file_path, "Content-Type": "application/octet-stream"}) as session:
                    response = await session.put("/api/fs/put", data=content.getvalue())
                    response.raise_for_status()
                    data = await response.json()
                    if data["code"] != 200:
                        raise aiohttp.ClientResponseError(status=data["code"], request_info=response.request_info, history=response.history)
                    size = await getSize()
                    if size == file.size:
                        return True
                    else:
                        logger.terror("storage.error.alist.write_file.size_mismatch", file=file.hash, file_size=humanize.naturalsize(file.size, binary=True), actual_file_size=humanize.naturalsize(size, binary=True))
                        return False
            except Exception as e:
                logger.terror("storage.error.alist.write_file.retry", file=file.hash, e=e, retry=delay)
            await asyncio.sleep(delay)
        return False

    async def recycleFiles(files):
        pass