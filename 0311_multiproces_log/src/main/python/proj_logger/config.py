import logging
import logging.config
from pathlib import Path

# if __package__:
from .formatters import ColoredFormatter
from .utils import test_err, test_msg
# else:
#     from formatters import ColoredFormatter    
#     from utils import test_err, test_msg

cfg_logger = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "class": "logging.Formatter",
            "format": "%(asctime)s [%(levelname)+8s][%(filename)+20s][%(funcName)+15s:%(lineno)+3s] : %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(asctime)s [%(levelname)s] : %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "colored": {
            "()" : ColoredFormatter,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "log.log",
            "formatter": "detailed",
            "level": "DEBUG"
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    },
}
def setup_logger(log_name:str):
    logger = logging.getLogger(log_name)  # Logger name is process name
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter(datefmt = "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(console_handler)
    
    file_handler = logging.FileHandler(f"process_{log_name}.log")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt = "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_handler)

    logger.info(f"Process {log_name} started.")
    
    
    
def set_log_file(log_path: str):
    Path(log_path).mkdir(parents=True, exist_ok=True)
    cfg_logger["handlers"]["file"]["filename"] = f'{Path(log_path)/"log.log"}'

def setlogger(log_path :str=None, debug_mode: bool=False):
    if log_path: 
        set_log_file(log_path)
    
    if debug_mode: 
        cfg_logger["handlers"]["console"]["level"] = "DEBUG"
    
    logging.config.dictConfig(cfg_logger)

def test_log():
    test_err()
    test_msg()

if __name__ == "__main__":
    setlogger(debug_mode=True)
    test_log()
    

