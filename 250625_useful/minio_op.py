import logging
import pickle
from io import BytesIO
from pathlib import Path

import pandas as pd
from minio import Minio

from utils import etag
from utils.retry import retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_CONTENT_TYPE = "application/octet-stream"


class FileHashMismatch(Exception):
    pass


class MinioController:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        secure=False,
    ):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
        self.bucket_name = bucket_name
        self._check_connection()

    def _check_connection(self):
        try:
            if self.client.bucket_exists(self.bucket_name):
                logger.info(f"Connect MinIO Bucket {self.bucket_name} Success")
            else:
                logger.error(f"Connect MinIO Bucket {self.bucket_name} Failed")
        except Exception as e:
            logger.error(f"Check MinIO Connection Failed: {e}", exc_info=True)

    @retry()
    def upload_file_from_local(
        self,
        remote_tag: str,
        local_file_path: str,
        content_type: str = DEFAULT_CONTENT_TYPE,
    ):
        file_size = Path(local_file_path).stat().st_size
        local_etag = etag.calculate_minio_etag_from_local(local_file_path)

        resp = self.client.fput_object(
            self.bucket_name,
            remote_tag,
            local_file_path,
            content_type=content_type,
        )

        if local_etag != resp.etag:
            raise FileHashMismatch(f"[{local_file_path}] Etag Mismatch: {local_etag} != {resp.etag}")

        logger.info(f"File: {local_file_path}")
        logger.info(f"Tag: {resp.object_name}")
        logger.info(f"File Size: {file_size} bytes")
        logger.info(f"Version: {resp.version_id}")
        logger.info(f"ETAG: {resp.etag}")

        return resp

    @retry()
    def upload_file_from_byte(
        self,
        remote_tag: str,
        data_bytes: bytes,
        content_type: str = DEFAULT_CONTENT_TYPE,
    ):
        local_etag = etag.calculate_minio_etag(data_byte)
        data_stream = BytesIO(data_bytes)
        file_size = len(data_bytes)

        resp = self.client.put_object(
            self.bucket_name,
            remote_tag,
            data_stream,
            file_size,
            content_type=content_type,
        )

        if local_etag != resp.etag:
            raise FileHashMismatch(f"Etag Mismatch: {local_etag} != {resp.etag}")
        logger.info(f"Tag: {resp.object_name}")
        logger.info(f"File Size: {file_size} bytes")
        logger.info(f"Version: {resp.version_id}")
        logger.info(f"ETAG: {resp.etag}")

        return resp

    @retry()
    def upload_file_from_df(
        self,
        remote_tag: str,
        df_data: pd.DataFrame,
        content_type: str = DEFAULT_CONTENT_TYPE,
    ):
        data_bytes = pickle.dumps(df_data)
        local_etag = etag.calculate_minio_etag(data_byte)

        data_stream = BytesIO(data_bytes)
        file_size = len(data_bytes)

        resp = self.client.put_object(
            self.bucket_name,
            remote_tag,
            data_stream,
            file_size,
            content_type=content_type,
        )

        if local_etag != resp.etag:
            raise FileHashMismatch(f"Etag Mismatch: {local_etag} != {resp.etag}")

        logger.info(f"Tag: {resp.object_name}")
        logger.info(f"File Size: {file_size} bytes")
        logger.info(f"Version: {resp.version_id}")
        logger.info(f"ETAG: {resp.etag}")

        return resp

    @retry()
    def download_df(
        self,
        remote_tag: str,
    ):
        stat = self.client.stat_object(self.bucket_name, remote_tag)
        resp = self.client.get_object(self.bucket_name, remote_tag)

        local_etag = etag.calculate_minio_etag(resp.data)

        logger.info(f"Tag: {stat.object_name}")
        logger.info(f"File Size: {stat.size} bytes")
        logger.info(f"Version: {stat.version_id}")
        logger.info(f"ETAG: {stat.etag}")

        if stat.etag != local_etag:
            raise FileHashMismatch(f"Etag Mismatch: {stat.etag} != {local_etag}")

        try:
            res = pickle.loads(resp.data)
            if isinstance(res, pd.DataFrame):
                return res
            else:
                raise TypeError(f"[{remote_tag}] is not a DataDrame")
        except pickle.UnpicklingError:
            res = pd.read_csv(BytesIO(resp.data))
            return res


if __name__ == "__main__":
    import pandas as pd

    MINIO_ENDPOINT = "localhost:9000"
    MINIO_ACCESS_KEY = "minioadmin"
    MINIO_SECRET_KEY = "minioadmin"
    MINIO_BUCKET_NAME = "3d-bucket"

    mc = MinioController(MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME)

    filename = "./data.csv"
    data = pd.read_csv(filename)
    data_byte = pickle.dumps(data)

    resp_local = mc.upload_file_from_local("data_local.csv", filename, content_type="application/csv")

    resp = mc.upload_file_from_byte("data.csv", data_byte)

    resp = mc.upload_file_from_df("data.csv", data)

    resp = mc.download_df("data.csv")
    logger.info(f"Shape: {resp.shape}")

    resp = mc.download_df("data_local.csv")
    logger.info(f"Shape: {resp.shape}")
