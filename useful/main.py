import logging
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from minio import Minio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DELETE_VERSION = False
DELETE_VERSION = True


class MinioFolderSync:
    def __init__(self, endpoint, access_key, secret_key, bucket_name, secure=False):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
        self.bucket_name = bucket_name
        self._check_connection()

    def _check_connection(self):
        try:
            if self.client.bucket_exists(self.bucket_name):
                logger.info("Initization MinIO Success")
                for _ in self.client.list_objects(self.bucket_name):
                    logger.info("Get Object Success")
                    break
                else:
                    logger.info("Get Object Failed")

        except Exception as e:
            logger.error(f"Initization MinIO Failed: {e}", exc_info=True)

    def upload_dir(self, src: str, minio_prefix: str = ""):
        path_src = Path(src)
        if not path_src.is_dir():
            logger.info(f"[{src}] is not a Valid Directory")
            return

        for item in path_src.rglob("*"):
            if item.is_file():
                obj_name = (minio_prefix / item.relative_to(src)).as_posix()
                try:
                    logger.info(f"Upload [{item}] to [{obj_name}]")
                    self.client.fput_object(self.bucket_name, obj_name, item)
                except Exception as e:
                    logger.error(f"Upload [{item}] Failed : {e}", exc_info=True)

    def _upload_zip(self, member: ZipInfo, zf: ZipFile, minio_prefix: str):
        if member.is_dir():
            return
        try:
            file_name = member.filename
            obj_name = (minio_prefix / Path(file_name)).as_posix()
            logger.info(f"Upload File [{file_name}] to [{obj_name}]")
            with zf.open(member) as f:
                zf_data = f.read()
                self.client.put_object(self.bucket_name, obj_name, BytesIO(zf_data), length=len(zf_data))
        except Exception as e:
            logger.error(f"Upload File [{file_name}] Failed: {e}", exc_info=True)

    def upload_from_zip(self, zf_byte: bytes, minio_prefix: str) -> None:
        with ZipFile(BytesIO(zf_byte), "r") as zf:
            for member in zf.infolist():
                self._upload_zip(member, zf, minio_prefix)

    def download_dir(self, minio_dir: str, local_dir: str):
        if minio_dir == "":
            logger.info("Can Not Download Root Folder")
            return
        try:
            lst_obj = self.client.list_objects(self.bucket_name, prefix=minio_dir, recursive=True)
            lst_obj = list(lst_obj)
            cnt_obj = len(lst_obj)
            cnt = 0
            for obj in lst_obj:
                cnt += 1
                obj_name = obj.object_name
                relative_path = Path(obj_name).relative_to(minio_dir)
                local_file_path = Path(local_dir) / relative_path
                try:
                    logger.info(f"[{cnt}/{cnt_obj}] Download [{obj_name}] to [{local_file_path}]")
                    local_file_path.parent.mkdir(parents=True, exist_ok=True)
                    self.client.fget_object(self.bucket_name, obj_name, local_file_path)
                except Exception as e:
                    logger.error(f"Download [{obj_name}] Failed : {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)

    def download_to_zip(self, minio_dir: str, local_dir: str):
        zip_file = Path(local_dir) / "result.zip"
        zip_file.parent.mkdir(exist_ok=True, parents=True)
        if minio_dir == "":
            logger.info("Can Not Download Root Folder")
            return
        
        if "[recursive]" in minio_dir:
            use_recursive=True
            minio_dir = minio_dir.replace("[recursive]", "")
        else:
            use_recursive=False

        try:
            lst_obj = self.client.list_objects(self.bucket_name, prefix=minio_dir, recursive=use_recursive)
            lst_obj = list(lst_obj)
            cnt_obj = len(lst_obj)
            cnt = 0
            with ZipFile(zip_file, "w", ZIP_DEFLATED) as zf:
                for obj in lst_obj:
                    cnt += 1
                    obj_name = obj.object_name
                    logger.info(f"[{cnt}/{cnt_obj}] Download [{obj_name}] to Zip File")
                    try:
                        resp = self.client.get_object(self.bucket_name, obj_name)
                        file_content = resp.read()
                        zf.writestr(obj_name, file_content)
                    except Exception as e:
                        logger.error(f"Download [{obj_name}] Failed : {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)

    def delete_objs(self, minio_prefix: str):
        if minio_prefix == "":
            logger.info("Can Not Delete Root Folder")
            return

        try:
            objs = self.client.list_objects(self.bucket_name, prefix=minio_prefix, recursive=True)
            lst_obj = [obj.object_name for obj in objs]
            logger.info(f"Found {len(lst_obj)} object: {lst_obj}")

            for obj in lst_obj:
                lst_obj_ver = self.client.list_objects(self.bucket_name, prefix=obj, include_version=True)
                lst_ver = [ver.version_id for ver in lst_obj_ver]
                logger.info(f"Object [{obj}] has {len(lst_ver)} version")

                if DELETE_VERSION:
                    for ver in lst_ver:
                        self.client.remove_object(self.bucket_name, obj, ver)
                else:
                    self.client.remove_object(self.bucket_name, obj)

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)


if __name__ == "__main__":
    MINIO_ENDPOINT = "localhost:9000"
    MINIO_ACCESS_KEY = "minioadmin"
    MINIO_SECRET_KEY = "minioadmin"
    MINIO_BUCKET_NAME = "test"

    mcc = MinioFolderSync(MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME)

    TEST_DIR = "test_data"
    SUB_DIR1 = "inner_folder1"
    SUB_DIR2 = "inner_folder2"
    path_test = Path(TEST_DIR)
    path_sub1 = path_test / SUB_DIR1
    path_sub2 = path_test / SUB_DIR2
    path_sub1.mkdir(exist_ok=True, parents=True)
    path_sub2.mkdir(exist_ok=True, parents=True)

    with open(path_test / "test1.txt", "w") as f:
        f.write("TEST TXT1\nTEST TXT1")
    with open(path_sub1 / "test2.txt", "w") as f:
        f.write("TEST TXT2\nTEST TXT2")
    with open(path_sub2 / "data.csv", "w") as f:
        f.writelines(["Part, Lot\n", "a, 1\n", "b, 2\n"])

    # logger.info("Upload Directory")
    SRC = TEST_DIR
    MINIO_PREFIX = "test_upload/from_dir"
    mcc.upload_dir(SRC, MINIO_PREFIX)

    logger.info("Download Directory")
    MINIO_DIR = MINIO_PREFIX
    LOCAL_DIR = "download_from_minio"
    mcc.download_dir(MINIO_DIR, LOCAL_DIR)

    # logger.info("Download Directory to Zip")
    MINIO_DIR = MINIO_PREFIX + "/test1.txt"
    # MINIO_DIR = MINIO_PREFIX + "[recursive]"
    # MINIO_DIR = MINIO_PREFIX
    LOCAL_DIR = "download_from_minio_zip"
    mcc.download_to_zip(MINIO_DIR, LOCAL_DIR)

    # logger.info("Upload from Zip")
    # MINIO_PREFIX = "test_upload/from_zip"
    # with open((LOCAL_DIR + "/result.zip"), "rb") as zip_file:
    #     mcc.upload_from_zip(zip_file.read(), MINIO_PREFIX)

    # logger.info("Delete Data in Minio")
    # MINIO_PREFIX = "test_upload/from_dir"
    # MINIO_PREFIX = "test_upload/from_dir/test1.txt"

    # MINIO_PREFIX = ""
    # mcc.delete_objs(MINIO_PREFIX)

    logger.info("Done")
