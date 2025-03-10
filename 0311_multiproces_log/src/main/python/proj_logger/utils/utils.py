import logging

logger = logging.getLogger(__name__)

def test_err():
    logger.debug("----- Testing Error -----")
    try:
        _ = 1/0
    except Exception as e:
        logger.error(f'Error: {e}', exc_info=True)

def test_msg():
    logger.debug("----- Testing Message -----")
    logger.debug("This is DEBUG")
    logger.info("This is INFO")
    logger.warning("This is WARN")
    logger.error("This is ERROR")
    logger.critical("This is CRITICAL")
