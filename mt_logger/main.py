import logging
import logging.config
from logCFG import my_logging_dict
import threading
import time

logging.config.dictConfig(my_logging_dict)
logger = logging.getLogger(__name__)

class UploaderThread(threading.Thread):
    def __init__(self, _log, log_init=None, *args, **kwargs) -> None:
        super(UploaderThread, self).__init__(*args, **kwargs)
        self._log = _log
        self.logger = logging.getLogger("MT_Logger")
        if log_init:
            log_init(self.logger)

    def run(self):
        logger=self.logger
        while True:
            logger.info(f'Uploading {self._log}')
            foo()
            time.sleep(2)

def foo():
    logger.info("THIS IS FOO")
    
def logger_configurer(logger):
    _handler = logging.FileHandler(f"upload_log.txt")
    _handler.setLevel(logging.DEBUG)
    _formatter = logging.Formatter("{asctime:s} [{levelname:>8s}][{filename:>20s}][{processName}|{threadName}][{funcName:>20s}:{lineno:4d}] - {message}", style="{")
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)
    logger.info("ADD LOGGER")

def main():
    logger.info("This is main")
    uploader = UploaderThread(name="Uploader", _log="test", log_init=logger_configurer, daemon=True)
    uploader.start()
    
    while uploader.is_alive(): 
        uploader.join(3)
        logger.info("This is main, waiting")
    

if __name__ == "__main__":
    main()