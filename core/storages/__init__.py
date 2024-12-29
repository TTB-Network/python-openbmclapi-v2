from core.classes import Storage
from core.storages.local import LocalStorage
from core.storages.alist import AListStorage
from core.config import Config
from typing import List


def getStorages() -> List[Storage]:
    config = Config.get("storages")
    storages = []
    for storage in config:
        if storage["type"] == "local":
            storages.append(LocalStorage(path=storage["path"]))
        if storage["type"] == "alist":
            storages.append(
                AListStorage(
                    username=storage["username"],
                    password=storage["password"],
                    url=storage["url"],
                    path=storage["path"],
                )
            )
    return storages
