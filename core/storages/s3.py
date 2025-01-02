from core.classes import Storage, FileInfo, FileList
from core.logger import logger
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import Literal, Union
from tqdm import tqdm
import boto3
import humanize
import io
import asyncio
import secrets


class S3Storage(Storage):
    def __init__(
        self,
        endpoint: str,
        access_key_id: str,
        secret_access_key: str,
        signature_version: str,
        bucket: str,
        addressing_style: Literal["auto", "path", "virtual"] = "auto",
        session_token: Union[None, str] = None,
    ):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token,
            endpoint_url=endpoint,
            config=Config(s3={"addressing_style": addressing_style}, signature_version=signature_version),
        )
        self.bucket = bucket

    async def init(self) -> None:
        pass

    async def writeFile(
        self, file: FileInfo, content: io.BytesIO, delay: int, retry: int
    ) -> bool:
        file_path = f"{file.hash[:2]}/{file.hash}"
        try:
            response = self.client.head_object(Bucket=self.bucket, Key=file_path)
            if response["ContentLength"] == len(content.getvalue()):
                return True
        except Exception:
            pass

        for _ in range(retry):
            try:
                self.client.put_object(Bucket=self.bucket, Key=file_path, Body=content.getbuffer())
                response = self.client.head_object(Bucket=self.bucket, Key=file_path)
                uploaded_size = response["ContentLength"]
                if uploaded_size == file.size:
                    return True
                else:
                    logger.terror(
                        "storage.error.s3.write_file.size_mismatch",
                        file=file.hash,
                        file_size=humanize.naturalsize(file.size, binary=True),
                        actual_file_size=humanize.naturalsize(uploaded_size, binary=True),
                    )
                    return False

            except ClientError as e:
                logger.terror(
                    "storage.error.s3.write_file.retry",
                    file=file.hash,
                    e=e,
                    retry=delay,
                )

            await asyncio.sleep(delay)

        logger.terror("storage.error.s3.write_file.failed", file=file.hash)
        return False

    async def check(self) -> None:
        file_path = secrets.token_hex(8)
        try:
            self.client.put_object(Bucket=self.bucket, Key=file_path, Body=b"")
            self.client.head_object(Bucket=self.bucket, Key=file_path)
            self.client.delete_object(Bucket=self.bucket, Key=file_path)
            logger.tsuccess("storage.success.s3.check")
        except Exception as e:
            logger.terror("storage.error.s3.check", e=e)
    
    async def getMissingFiles(self, files: FileList, pbar: tqdm) -> FileList:
        async def checkFile(file: FileInfo, pbar: tqdm) -> bool:
            pbar.update(1)
            file_path = f"{file.hash[:2]}/{file.hash}"
            try:
                response = self.client.head_object(Bucket=self.bucket, Key=file_path)
                s3_file_size = response["ContentLength"]
                return s3_file_size != file.size
            except Exception:
                pass

        results = await asyncio.gather(*[checkFile(file, pbar) for file in files.files])
        missing_files = [
            file for file, is_missing in zip(files.files, results) if is_missing
        ]
        return FileList(files=missing_files)
