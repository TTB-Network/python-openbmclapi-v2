from core.classes import Storage, FileInfo, FileList
from core.logger import logger
from core.i18n import locale
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import Literal, Union, Self
from tqdm import tqdm
from aiohttp import web
from pathlib import Path
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
        s3_files = {}
        try:
            paginator = self.client.get_paginator("list_objects_v2")
            # Use asyncio.to_thread to run synchronous paginator in thread pool
            for page in paginator.paginate(Bucket=self.bucket):
                for obj in page.get("Contents", []):
                    s3_files[obj["Key"]] = obj["Size"]
        except ClientError as e:
            logger.terror("storage.error.s3.get_s3_files", e=e)

        missing_files = []
        for file in files.files:
            file_key = f"{file.hash[:2]}/{file.hash}"
            if file_key not in s3_files or s3_files[file_key] != file.size:
                missing_files.append(file)
            pbar.update(1)
        
        return FileList(files=missing_files)

    async def express(self, hash: str, counter: dict) -> Union[web.Response, web.FileResponse]:
        file_key = f"{hash[:2]}/{hash}"
        try:
            # Generate a presigned URL for the file
            response = await asyncio.to_thread(
                self.client.head_object,
                Bucket=self.bucket,
                Key=file_key
            )
            file_size = response["ContentLength"]
            
            # Generate presigned URL for downloading the file
            url = await asyncio.to_thread(
                self.client.generate_presigned_url,
                "get_object",
                Params={"Bucket": self.bucket, "Key": file_key},
                ExpiresIn=3600  # URL valid for 1 hour
            )
            
            # Return redirect to presigned URL
            response = web.HTTPFound(url)
            response.headers["x-bmclapi-hash"] = hash
            counter["bytes"] += file_size
            counter["hits"] += 1
            return response
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return web.HTTPNotFound()
            logger.terror("storage.error.s3.express", hash=hash, e=e)
            return web.HTTPError(text=str(e))
        except Exception as e:
            logger.terror("storage.error.s3.express", hash=hash, e=e)
            return web.HTTPError(text=str(e))

    async def recycleFiles(self, files: FileList) -> None:
        """Clean up files in S3 that are not in the valid file list"""
        delete_files = []
        
        # Get all valid file keys
        valid_keys = {
            f"{file.hash[:2]}/{file.hash}"
            for file in files.files
        }
        
        # List all files in S3 bucket
        try:
            paginator = self.client.get_paginator("list_objects_v2")
            all_s3_keys = []
            for page in paginator.paginate(Bucket=self.bucket):
                for obj in page.get("Contents", []):
                    all_s3_keys.append(obj["Key"])
        except ClientError as e:
            logger.terror("storage.error.s3.recycle.list", e=e)
            return
        
        # Find files to delete
        with tqdm(
            desc=locale.t("storage.tqdm.desc.recycling_check"),
            total=len(all_s3_keys),
            unit_scale=True,
            unit=locale.t("storage.tqdm.unit.files"),
        ) as pbar:
            for key in all_s3_keys:
                pbar.update(1)
                if key not in valid_keys:
                    delete_files.append(key)
        
        if len(delete_files) == 0:
            logger.tinfo("storage.success.s3.no_need_to_recycle")
            return
        
        # Delete files in batches (S3 allows max 1000 objects per delete request)
        with tqdm(
            desc=locale.t("storage.tqdm.desc.recycling"),
            total=len(delete_files),
            unit_scale=True,
            unit=locale.t("storage.tqdm.unit.files"),
        ) as pbar:
            total_size = 0
            for i in range(0, len(delete_files), 1000):
                batch = delete_files[i:i+1000]
                try:
                    # Get sizes before deleting
                    for key in batch:
                        try:
                            response = self.client.head_object(Bucket=self.bucket, Key=key)
                            total_size += response["ContentLength"]
                        except Exception:
                            pass
                    
                    # Delete batch
                    self.client.delete_objects(
                        Bucket=self.bucket,
                        Delete={
                            "Objects": [{"Key": key} for key in batch],
                            "Quiet": True
                        }
                    )
                    pbar.update(len(batch))
                except ClientError as e:
                    logger.terror("storage.error.s3.recycle", e=e)
            
            logger.tsuccess(
                "storage.success.s3.recycled",
                size=humanize.naturalsize(total_size, binary=True),
            )