import ftplib
import logging
from pathlib import Path
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


class FTPClient:
    def __init__(self, url: str, user: str, pwd: str):
        self.ftp = ftplib.FTP(url)
        self.ftp.login(user, pwd)
        self.ftp_welcome = self.ftp.getwelcome()
        logger.debug(f"FTPClient {id(self)} Welcome: {self.ftp_welcome}")

    # region Download
    @staticmethod
    def walk_ftp_dir(ftp: ftplib.FTP, dir_remote: str, recursive: bool = True) -> tuple[list[str], dict]:
        lst_file = list()
        dic_dir = defaultdict(list)
        cnt_depth = 0

        def recursive_list_dir(ftp: ftplib.FTP, dir_cur: str, recursive: bool = True):
            nonlocal lst_file, dic_dir, cnt_depth
            if not recursive and cnt_depth > 0:
                return
            try:
                ftp.cwd(dir_cur)
            except ftplib.error_perm as e:
                logger.error(f"Change FTP Directory to [{dir_cur}] Failed: {e}", exc_info=True)
                return

            for obj_info in ftp.mlsd(facts=["type"]):
                obj_name, obj_type = obj_info[0], obj_info[1]["type"]
                if obj_type == "dir":
                    logger.debug(f"[{cnt_depth}] Found Directory : {obj_name}")
                    dic_dir[cnt_depth].append(f"{ftp.pwd()}/{obj_name}")
                    cnt_depth += 1
                    recursive_list_dir(ftp, obj_name, recursive)
                    ftp.cwd("..")
                elif obj_type == "file":
                    _file = f"{ftp.pwd()}/{obj_name}"
                    logger.debug(f"[{cnt_depth}] Found File      : {_file}")
                    lst_file.append(_file)
                else:
                    logger.warning(f"Unknown Type: {obj_name}")
            cnt_depth -= 1

        recursive_list_dir(ftp, dir_remote, recursive)
        return lst_file, dict(dic_dir)

    def download_ftp_file(self, dir_remote: str, dir_local: str, recursive: bool = True):
        self.ftp.cwd("/")
        # Get File List
        logger.info(f"Walking Remote Directory [{dir_remote}] with recursive is {recursive}")
        lst_file, dic_dir = self.walk_ftp_dir(self.ftp, dir_remote, recursive)
        logger.info(f"Found Directory: {dic_dir}")
        logger.info(f"Get File List: {lst_file}")

        # Download File
        logger.info("Start Download Files in File List")
        cnt_downloaded = 0
        for idx, file in enumerate(lst_file):
            _batch = f"[{idx + 1:2d}/{len(lst_file):2d}]"
            try:
                path_file = Path(dir_local) / file.lstrip(dir_remote).lstrip("/")
                path_file.parent.mkdir(parents=True, exist_ok=True)
                logger.info(f"{_batch} Download File [{file}] to [{path_file}]")
                with open(path_file, "wb") as f:
                    self.ftp.retrbinary(f"RETR {file}", f.write)
                cnt_downloaded += 1
            except Exception as e:
                logger.error(f"{_batch} Error : {e}", exc_info=True)

        self.ftp.cwd("/")
        logger.info(f"Download Task Finished: {cnt_downloaded}/{len(lst_file)}")

    # endregion Download

    # region Upload
    def upload_local_file(self, dir_upload: str, dir_remote: str):
        self.ftp.cwd("/")
        logger.info(f"Start Upload Files from [{dir_upload}]")
        cnt_depth = 0
        cnt_uploaded = 0

        def walk_upload_dir(dir_cur: str, dir_cur_remote: str):
            nonlocal cnt_depth, cnt_uploaded
            logger.info(f"Upload Object in [{dir_cur}] to [{dir_cur_remote}]")

            try:
                self.ftp.cwd(dir_cur_remote)
                logger.info(f"Change FTP Directory to [{dir_cur_remote}]")
            except ftplib.error_perm:
                self.ftp.mkd(dir_cur_remote)
                self.ftp.cwd(dir_cur_remote)
                logger.info(f"Create and Change FTP Directory [{dir_cur_remote}]")
            except Exception as e:
                logger.error(f"Change FTP Directory to [{dir_cur_remote}] Failed: {e}", exc_info=True)

            for obj in Path(dir_cur).glob("*"):
                if obj.is_dir():
                    logger.info(f"[{cnt_depth}] Object {obj} is Directory")
                    cnt_depth += 1
                    walk_upload_dir(obj, obj.name)
                    self.ftp.cwd("..")
                else:
                    remote_file = Path(self.ftp.pwd()) / obj.name
                    logger.info(f"[{cnt_depth}] Upload: {obj} to {remote_file}")
                    try:
                        with open(obj, "rb") as f:
                            self.ftp.storbinary(f"STOR {obj.name}", f)
                        cnt_uploaded += 1
                    except Exception as e:
                        logger.error(f"Upload Error: {e}", exc_info=True)
            cnt_depth -= 1

        walk_upload_dir(dir_upload, dir_remote)
        self.ftp.cwd("/")
        logger.info(f"Uploaded {cnt_uploaded} Files")

    # endregion Upload

    def disconnect(self):
        if hasattr(self, "ftp"):
            try:
                logger.debug(f"FTPClient {id(self)} Disconnecting...")
                self.ftp.quit()
            except ftplib.all_errors as e:
                logger.error(f"FTP Error: {e}", exc_info=True)
            except Exception as e:
                logger.error(f"Error: {e}", exc_info=True)
            finally:
                self.ftp = None

    def __del__(self):
        self.disconnect()
        logger.debug(f"FTPClient {id(self)} Exit")


if __name__ == "__main__":
    FTP_URL = "localhost"
    FTP_USER = "ituser"
    FTP_PWD = "0000"

    DIR_REMOTE = "CDSC/dummy1/dummy2"
    DIR_REMOTE_UPLOAD = "CDSC/2021/09/01/0001"
    DIR_LOCAL = "jobId123/res/tool_file"
    DIR_UPLOAD = "jobId123/res/to_upload"

    ftp_client = FTPClient(FTP_URL, FTP_USER, FTP_PWD)
    ftp_client.download_ftp_file(DIR_REMOTE, DIR_LOCAL)
    ftp_client.upload_local_file(DIR_UPLOAD, DIR_REMOTE_UPLOAD)
