import hashlib
import logging
import math
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from minio import Minio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_PART_SIZE = 5 * 1024 * 1024


def calculate_minio_etag_from_local(local_file_path: str, part_size: int = DEFAULT_PART_SIZE):
    file_size = Path(local_file_path).stat().st_size

    if file_size <= part_size:
        with open(local_file_path, "rb") as f:
            md5_hash = hashlib.md5(f.read())
        return md5_hash.hexdigest()
    else:
        part_md5s = []
        with open(local_file_path, "rb") as f:
            while True:
                chunk = f.read(part_size)
                if not chunk:
                    break
                part_md5s.append(hashlib.md5(chunk).digest())

        concatenated_md5s = b"".join(part_md5s)
        final_md5 = hashlib.md5(concatenated_md5s).hexdigest()
        return f"{final_md5}-{len(part_md5s)}"


def calculate_minio_etag(data_bytes: bytes, part_size: int = DEFAULT_PART_SIZE):
    file_size = len(data_bytes)

    if file_size <= part_size:
        return hashlib.md5(data_bytes).hexdigest()
    else:
        num_parts = math.ceil(file_size / part_size)
        part_md5s = []
        for i in range(num_parts):
            start = i * part_size
            end = min((i + 1) * part_size, file_size)
            part_data = data_bytes[start:end]
            part_md5s.append(hashlib.md5(part_data).digest())

        concatenated_md5s = b"".join(part_md5s)
        final_md5 = hashlib.md5(concatenated_md5s).hexdigest()
        return f"{final_md5}-{len(part_md5s)}"


class MC:
    def __init__(self, endpoint, access_key, secret_key, bucket_name, secure=False):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
        self.bucket_name = bucket_name
        self._check_connection()

    def _check_connection(self):
        try:
            if self.client.bucket_exists(self.bucket_name):
                logger.info("Acceess Bucket Success")
                for _ in self.client.list_objects(self.bucket_name):
                    logger.info("Access Object Success")
                    break
                else:
                    logger.info("Access Object Failed")
            else:
                logger.info("Acceess Bucket Failed")
        except Exception:
            logger.error("Initization MinIO Failed", exc_info=True)

    def upload_file_from_local(
        self,
        remote_tag: str,
        local_file_path: str,
        content_type: str = "application/octet-stream",
    ):
        resp = self.client.fput_object(
            self.bucket_name,
            remote_tag,
            local_file_path,
            content_type=content_type,
        )

        return resp

    def upload_file(
        self,
        remote_tag: str,
        data_bytes: bytes,
        content_type: str = "application/octet-stream",
    ):
        data_stream = BytesIO(data_bytes)
        data_length = len(data_bytes)

        resp = self.client.put_object(
            self.bucket_name,
            remote_tag,
            data_stream,
            data_length,
            content_type=content_type,
        )

        return resp


if __name__ == "__main__":
    import pandas as pd

    MINIO_ENDPOINT = "localhost:9000"
    MINIO_ACCESS_KEY = "minioadmin"
    MINIO_SECRET_KEY = "minioadmin"
    MINIO_BUCKET_NAME = "test"

    mcc = MC(MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME)

    filename = "./data.csv"
    data = pd.read_csv(filename)
    data_byte = data.to_csv(index=False).encode("utf-8")

    resp_local = mcc.upload_file_from_local("data_local.csv", filename)
    local_etag = calculate_minio_etag_from_local(filename)
    logger.info(f"MinIO ETAG: {resp_local.etag}")
    logger.info(f"Local ETAG: {local_etag}")
    logger.info(f"ETAG Same: {resp_local.etag == local_etag}")

    resp = mcc.upload_file("data.csv", data_byte)
    local_etag = calculate_minio_etag(data_byte)
    logger.info(f"MinIO ETAG: {resp.etag}")
    logger.info(f"Local ETAG: {local_etag}")
    logger.info(f"ETAG Same: {resp.etag == local_etag}")
