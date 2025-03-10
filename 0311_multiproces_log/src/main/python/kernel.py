import logging
import time

def foo(logger_name):
    logger = logging.getLogger(logger_name)
    logger.info(f"{logger_name} - foo")
    time.sleep(2)
    logger.info(f"{logger_name} - foo done")
    