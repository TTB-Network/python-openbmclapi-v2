from core.classes import Storage, FileInfo, FileList
from core.logger import logger
from core.i18n import locale
from aiohttp import web
from typing import Any, Dict
from tqdm import tqdm
from pathlib import Path
import os
import io
import aiofiles
import asyncio
import tempfile
import humanize


class LocalStorage(Storage):
    def __init__(self, path: str) -> None:
        self.path = path

    async def init(self) -> None:
        os.makedirs(self.path, exist_ok=True)

    async def check(self) -> None:
        logger.tinfo("storage.info.local.check")
        try:
            with tempfile.NamedTemporaryFile(dir=self.path, delete=True) as temp_file:
                temp_file.write(b"")
            logger.tsuccess("storage.success.local.check")
        except Exception as e:
            raise Exception(locale.t("storage.error.local.check", e=e))

    async def writeFile(
        self, file: FileInfo, content: io.BytesIO, delay: int, retry: int
    ) -> bool:
        file_path = os.path.join(self.path, file.hash[:2], file.hash)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if Path(file_path).exists and Path(file_path).stat().st_size == len(
            content.getvalue()
        ):
            return True
        for _ in range(retry):
            try:
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(content.getbuffer())
                    await f.close()
                size = os.path.getsize(file_path)
                if size == file.size:
                    return True
                else:
                    logger.terror(
                        "storage.error.local.write_file.size_mismatch",
                        file=file.hash,
                        file_size=humanize.naturalsize(file.size, binary=True),
                        actual_file_size=humanize.naturalsize(size, binary=True),
                    )
                    return False
            except Exception as e:
                logger.terror(
                    "storage.error.local.write_file.retry",
                    file=file.hash,
                    e=e,
                    retry=delay,
                )

            await asyncio.sleep(delay)

        logger.terror("storage.error.local.write_file.failed", file=file.hash)
        return False

    async def getMissingFiles(self, files: FileList, pbar: tqdm) -> FileList:
        async def checkFile(file: FileInfo, pbar: tqdm) -> bool:
            pbar.update(1)
            file_path = os.path.join(self.path, file.hash[:2], file.hash)
            try:
                st = await asyncio.to_thread(os.stat, file_path)
                return st.st_size != file.size
            except FileNotFoundError:
                return True

        results = await asyncio.gather(*[checkFile(file, pbar) for file in files.files])
        missing_files = [
            file for file, is_missing in zip(files.files, results) if is_missing
        ]
        return FileList(files=missing_files)

    async def express(self, hash: str, counter: dict) -> web.Response:
        path = os.path.join(self.path, hash[:2], hash)
        if not os.path.exists(path):
            response = web.HTTPNotFound()
            return response
        try:
            file_size = os.path.getsize(path)
            response = web.FileResponse(path, status=200)
            response.headers["x-bmclapi-hash"] = hash
            counter["bytes"] += file_size
            counter["hits"] += 1
            return response
        except Exception as e:
            response = web.HTTPError(text=e)
            logger.debug(e)
            return response

    async def recycleFiles(self, files: FileList) -> None:
        delete_files = []

        valid_paths = {
            Path(os.path.join(self.path, file.hash[:2], file.hash)).resolve()
            for file in files.files
        }
        all_files = list(Path(self.path).rglob("*"))
        with tqdm(
            desc=locale.t("storage.tqdm.desc.recycling_check"),
            total=len(all_files),
            unit_scale=True,
            unit=locale.t("storage.tqdm.unit.files"),
        ) as pbar:
            for file in all_files:
                pbar.update(1)
                if file.is_file() and (file.resolve() not in valid_paths):
                    delete_files.append(file)

        if len(delete_files) == 0:
            logger.tinfo("storage.success.local.no_need_to_recycle")
            return

        with tqdm(
            desc=locale.t("storage.tqdm.desc.recycling"),
            total=len(delete_files),
            unit_scale=True,
            unit=locale.t("storage.tqdm.unit.files"),
        ) as pbar:
            size = 0
            for file in delete_files:
                size += file.stat().st_size
                pbar.update(1)
                try:
                    file.unlink()
                except Exception as e:
                    logger.terror("storage.error.local.recycle", e=e)

            logger.tsuccess(
                "storage.success.local.recycled",
                size=humanize.naturalsize(size, binary=True),
            )
