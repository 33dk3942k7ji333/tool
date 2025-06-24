import functools
import logging
import time

logger = logging.getLogger(__name__)

RETRY_TIME = 3


def retry(delay: float = 2):
    times = RETRY_TIME

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == times:
                        raise

                    logger.error(
                        f"[{i}/{RETRY_TIME}]Function [{func.__name__}] Failed : {e}, will retry in {delay} seconds"
                    )
                    time.sleep(delay)

        return wrapper

    return decorator
