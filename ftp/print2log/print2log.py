import contextlib
import functools
import logging
from typing import Any, Callable, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class StreamToLogger:
    def __init__(self, logger: logging.Logger, level: int = logging.INFO, msg: Optional[str] = None):
        self.logger = logger
        self.level = level
        self.msg = msg
        self.buffer = ""

    def _msg(self):
        if self.msg:
            return f"{self.msg} ---> [{self.buffer}]"
        else:
            return self.buffer

    def write(self, message: str):
        if message.endswith("\n"):
            self.buffer += message.rstrip("\n")
            if self.buffer:
                self.logger.log(self.level, self._msg())
            self.buffer = ""

        elif message.strip():
            self.buffer += message

    def flush(self):
        if self.buffer:
            self.logger.log(self.level, self._msg())
            self.buffer = ""


def redirect_to_logger(
    logger: logging.Logger | None = None,
    level: int = logging.INFO,
    msg: Optional[str] = None,
):
    """
    A decorator that redirects stdout into the specified logging system.

    Args:
        logger (logging.Logger | None): The Logger instance to use.
        level (int): The logging level to use.
        msg (Optional[str]): Message show before original stdout
    """

    _logger = logger if logger is not None else logging.getLogger()

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            stream_target = StreamToLogger(logger=_logger, level=level, msg=msg)
            with contextlib.redirect_stdout(stream_target):  # type: ignore
                result = func(*args, **kwargs)
            stream_target.flush()

            return result

        return wrapper  # type: ignore

    return decorator
