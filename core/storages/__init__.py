from core.classes import Storage
from core.storages.local import LocalStorage
from core.storages.alist import AListStorage
from core.storages.s3 import S3Storage
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
        if storage["type"] == "s3":
            storages.append(
                S3Storage(
                    endpoint=storage["endpoint"],
                    access_key_id=storage["access_key_id"],
                    secret_access_key=storage["secret_access_key"],
                    signature_version=storage.get("signature_version", "s3v4"),
                    bucket=storage["bucket"],
                    addressing_style=storage.get("addressing_style", "auto"),
                    session_token=storage.get("session_token", None),
                )
            )
    return storages
