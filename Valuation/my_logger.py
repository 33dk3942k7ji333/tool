import logging
import logging.config

dic_log_cfg = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "normal": {
            "style": "{",
            "format": "{asctime:s} [{levelname:.1s}][{filename:>10s}][{funcName:>10s}:{lineno:4d}] {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
    	},
	},
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "normal",
            "filename": "log.log",
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
    logging.config.dictConfig(dic_log_cfg)
    logger = logging.getLogger(__name__)
    logger.info('hello')