import hashlib
import logging
import math
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from minio import Minio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


if __name__ == "__main__":
    import pandas as pd

    MINIO_ENDPOINT = "localhost:9000"
    MINIO_ACCESS_KEY = "minioadmin"
    MINIO_SECRET_KEY = "minioadmin"
    MINIO_BUCKET_NAME = "3d-bucket"

    mcc = MC(MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME)
    print(mcc.client.get_bucket_lifecycle(MINIO_BUCKET_NAME))
    
    lifecycle_config = mcc.client.get_bucket_lifecycle(MINIO_BUCKET_NAME)
    for rule in lifecycle_config.rules: # type: ignore
        print(f"ID: {rule.rule_id}")
        print(f"Status: {'Enable' if rule.status == 'Enabled' else 'Disabale'}")
        if rule.expiration:
            print(f"Expiration Day: {rule.expiration.days}")
    
    stats = mcc.client.stat_object(MINIO_BUCKET_NAME, "data_local.csv")
    print(stats.last_modified)