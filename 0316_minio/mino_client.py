import logging
import os

from minio import Minio


class MinIOClient:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        secure: bool = False,
        logger: logging.Logger = None,
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket = bucket
        self.logger = logger if logger is not None else logging.getLogger(__name__)
        self._check_bucket()

    def _check_bucket(self):
        if self.client.bucket_exists(self.bucket):
            self.logger.info(f"Found Bucket [{self.bucket}]")
        else:
            self.logger.error(f"Bucket [{self.bucket}] not found")

    def upload_folder(self, dir_local: str, remote_prefix: str = ""):
        for root, _, files in os.walk(dir_local):
            for file in files:
                path_local = os.path.join(root, file)
                path_relative = os.path.relpath(path_local, dir_local)
                path_remote = os.path.join(remote_prefix, path_relative).replace("\\", "/")
                file_stat = os.stat(path_local)
                try:
                    self.logger.info(f"Upload [{path_local}] to [{path_remote}]")
                    with open(path_local, "rb") as f:
                        self.client.put_object(self.bucket, path_remote, f, file_stat.st_size)
                except Exception as e:
                    self.logger.error(f"Error: {e}", exc_info=True)

    def upload_file(self, path_local: str, file_tag: str):
        try:
            file_stat = os.stat(path_local)
            self.logger.info(f"Upload [{path_local}] to [{file_tag}]")
            with open(path_local, "rb") as f:
                self.client.put_object(self.bucket, file_tag, f, file_stat.st_size)
        except Exception as e:
            self.logger.error(f"Error: {e}", exc_info=True)

    def download_folder(self, remote_prefix: str, dir_local: str):
        objects = self.client.list_objects(self.bucket, prefix=remote_prefix, recursive=True)
        for obj in objects:
            try:
                path_remote = obj.object_name
                path_relative = os.path.relpath(path_remote, remote_prefix)
                path_local = os.path.join(dir_local, path_relative)
                os.makedirs(os.path.dirname(path_local), exist_ok=True)

                self.logger.info(f"Download [{path_remote}] to [{path_local}]")
                data = self.client.get_object(self.bucket, path_remote)
                with open(path_local, "wb") as file_data:
                    for d in data.stream(32 * 1024):
                        file_data.write(d)
            except Exception as e:
                self.logger.error(f"Error: {e}", exc_info=True)

    def download_file(self, file_tag: str, path_local: str):
        try:
            os.makedirs(os.path.dirname(path_local), exist_ok=True)
            self.logger.info(f"Download [{file_tag}] to [{path_local}]")
            data = self.client.get_object(self.bucket, file_tag)
            with open(path_local, "wb") as f:
                for d in data.stream(32 * 1024):
                    f.write(d)
        except Exception as e:
            self.logger.error(f"Error: {e}", exc_info=True)


if __name__ == "__main__":
    endpoint = "192.168.0.2:9000"
    bucket_name = "tpod"
    access_key = "minioadmin"
    secret_key = "minioadmin"

    client = MinIOClient(endpoint, access_key, secret_key, bucket_name)

    local_folder = "upload"
    remote_prefix = "upload_from/pc/in_minio"
    client.upload_folder(local_folder, remote_prefix)

    remote_prefix = "upload_from"
    download_folder = "down"
    client.download_folder(remote_prefix, download_folder)

    file_tag = "upload_from/pc/in_minio/l1/l2/we.zip"
    download_folder = "./test.zip"
    client.download_file(file_tag, download_folder)

    file_tag = "./test01.jpg"
    minio_tag = "test/test.jpg"
    client.upload_file(file_tag, minio_tag)
