from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod
from aiohttp import web
from tqdm import tqdm
from typing import Union
import io


@dataclass
class FileInfo:
    path: str
    hash: str
    size: int
    mtime: int


@dataclass
class FileList:
    files: List[FileInfo]


@dataclass
class AgentConfiguration:
    source: str
    concurrency: int


class Storage(ABC):
    @abstractmethod
    async def init(self) -> None:
        pass

    @abstractmethod
    async def check(self) -> None:
        pass

    @abstractmethod
    async def writeFile(
        self, file: FileInfo, content: io.BytesIO, delay: int, retry: int
    ) -> bool:
        pass

    @abstractmethod
    async def getMissingFiles(self, files: FileList, pbar: tqdm) -> FileList:
        pass

    @abstractmethod
    async def express(self,
        hash: str, counter: dict
    ) -> Union[web.Response, web.FileResponse]:
        pass

    @abstractmethod
    async def recycleFiles(self, files: FileList) -> None:
        pass
