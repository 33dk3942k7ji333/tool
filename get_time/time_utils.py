import time
import datetime
import functools
import logging

logger = logging.getLogger()

def timer_dec(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        total_time = time.perf_counter() - start_time
        logger.info(f'Function {func.__name__} Used {total_time:.2f} seconds')
        return result
    return wrapper

class TimeString:
    __today = datetime.date.today()
    __format = "%Y/%m/%d %H:%M:%S"
    
    @classmethod
    def getToday(cls, time_format=__format):
        return cls.__today.strftime(time_format)
    @classmethod
    def getYesday(cls, time_format=__format):
        time_yesday = cls.__today - datetime.timedelta(days=1)
        return time_yesday.strftime(time_format)
    @classmethod
    def getDaysAgo(cls, n, time_format=__format):
        time_yesday = cls.__today - datetime.timedelta(days=n)
        return time_yesday.strftime(time_format)    
    @classmethod
    def getNow(cls, time_format=__format):
        return datetime.datetime.now().strftime(time_format)
