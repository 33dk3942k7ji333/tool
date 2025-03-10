import logging

CSI = "\033["

def code2chars(code):
    return CSI + str(code) + "m"

class AnsiCode(object):
    def __init__(self):
        for name in dir(self):
            if not name.startswith("_"):
                value = getattr(self, name)
                setattr(self, name, code2chars(value))


class FontColor(AnsiCode):
    BLACK   = 30
    RED     = 31
    GREEN   = 32
    YELLOW  = 33
    BLUE    = 34
    MAGENTA = 35
    CYAN    = 36
    WHITE   = 37
    RESET   = 39


class Background(AnsiCode):
    BLACK   = 40
    RED     = 41
    GREEN   = 42
    YELLOW  = 43
    BLUE    = 44
    MAGENTA = 45
    CYAN    = 46
    WHITE   = 47
    RESET   = 49

    
class FontStyle (AnsiCode):
    BRIGHT  = 1
    DIM     = 2
    NORMAL  = 22
    RESET_ALL = 0


color = FontColor()
background = Background()
style = FontStyle()

COLORS = {
    "DEBUG":    color.GREEN,
    "INFO":     color.WHITE,
    "WARNING":  color.MAGENTA,
    "ERROR":    color.WHITE,
    "CRITICAL": color.RED,
}

MSG_FORMAT = {
    "DEBUG":    style.BRIGHT+COLORS["DEBUG"],
    "INFO":     style.BRIGHT+COLORS["INFO"],
    "WARNING":  style.BRIGHT+COLORS["WARNING"],
    "ERROR":    style.BRIGHT+background.RED+COLORS["ERROR"],
    "CRITICAL": style.BRIGHT+COLORS["CRITICAL"],
}

DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] : %(message)s"
TIME_FORMAT = f'{style.DIM}{color.YELLOW}%(asctime)s{style.RESET_ALL}'
FILE_FORMAT = "[%(filename)+20s:%(lineno)+3s]"

FORMATS = {
    "DEBUG":    f'{TIME_FORMAT} {MSG_FORMAT["DEBUG"]}[%(levelname)+8s]{FILE_FORMAT} - %(message)s{style.RESET_ALL}',
    "INFO":     f'{TIME_FORMAT} {MSG_FORMAT["INFO"]}[%(levelname)+8s]{style.RESET_ALL}{FILE_FORMAT} - %(message)s',
    "WARNING":  f'{TIME_FORMAT} {MSG_FORMAT["WARNING"]}[%(levelname)+8s]{style.RESET_ALL}{FILE_FORMAT} - %(message)s',
    "ERROR":    f'{TIME_FORMAT} {MSG_FORMAT["ERROR"]}[%(levelname)+8s]{FILE_FORMAT} - %(message)s{style.RESET_ALL}',
    "CRITICAL": f'{TIME_FORMAT} {MSG_FORMAT["CRITICAL"]}[%(levelname)+8s]{FILE_FORMAT} - %(message)s{style.RESET_ALL}',
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formatters = {level: logging.Formatter(fmt=f, **kwargs) for level, f in FORMATS.items()}

    def format(self, record: logging.LogRecord) -> str:
        return self.formatters[record.levelname].format(record)