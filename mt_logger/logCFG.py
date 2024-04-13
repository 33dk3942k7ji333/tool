import logging
import logging.config

my_logging_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "normal": {
            "style": "{",
            "format": "{asctime:s} [{levelname:>8s}][{filename:>20s}][{funcName:>20s}:{lineno:4d}] - {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
    	},
        "mp": {
            "style": "{",
            "format": "{asctime:s} [{levelname:>8s}][{filename:>20s}][{processName}|{threadName}][{funcName:>20s}:{lineno:4d}] - {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
	},
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "normal",
            "filename": "log.txt",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "normal",
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}




if __name__ == '__main__':
    logging.config.dictConfig(my_logging_dict)
    logger = logging.getLogger(__name__)
    logger.info('hello')
    logger.debug('hello - noshow')