import logging
from os import makedirs
from pathlib import Path
from typing import Union
from minio import Minio

logger = logging.getLogger(__name__)

class SingletonClass(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._initialized = False
        return cls._instance

    def clear(cls):
        delattr(cls.__class__, "_instance")
        delattr(cls.__class__, "_initialized")

class MinIOController(SingletonClass):
    def __init__(self, end_point: str, access_key: str, secret_key: str, bucket: Union[str, None]=None):
        if self._initialized: return
        self._initialized = True
        
        self.client = Minio(
            endpoint= end_point,
            access_key= access_key,
            secret_key= secret_key,
            secure= False,
            )
        
        self.root = Path.cwd()
        if bucket:
            self.__bucket = bucket
        else:            
            self.__bucket = None
        
    def set_bucket(self, bucket: str):
        self.__bucket = bucket
    
    def list_obj(self, prefix: str, recursive: bool=False):
        return (obj.object_name for obj in self.client.list_objects(self.__bucket, prefix=prefix, recursive=recursive))
    
    def download(self, source: str, target: str="./download", recursive: bool=True):
        dir_target = self.root/target
        makedirs(dir_target, exist_ok=True)
        for idx, _file in enumerate(self.list_obj(source, recursive=recursive)):
            logger.info(f'[{idx:>2d}]: Downloading {_file}')
            self.client.fget_object(self.__bucket, _file, dir_target/_file)
            
    def upload(self, dir_upload: str, prefix: str="", pattern="*"):
        path_upload = Path(dir_upload)
        cnt = 0
        for _file in path_upload.rglob(pattern):
            if not Path(_file).is_file():
                continue
            cnt += 1
            minio_tag = prefix + "/".join(list(_file.parts)[len(path_upload.parts):])
            logger.info(f'[{cnt:>2d}]: Uploading {_file.absolute()} to {minio_tag}')
            self.client.fput_object(self.__bucket, minio_tag, _file.absolute())
            
    # def clear(self):
    #     delattr(self.__class__, "_instance")
    #     delattr(self.__class__, "_initialized")
    #     delattr(self, "client")
