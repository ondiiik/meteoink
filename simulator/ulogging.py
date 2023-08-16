from usys import print_exception
from machine import RTC
from micropython import const


CRITICAL = const(5)
ERROR = const(4)
WARNING = const(3)
INFO = const(2)
DEBUG = const(1)
NOTSET = const(0)

_lvl = INFO
_lchr = "  ", "  ", "..", "??", "!!", "##"


class Logger:
    def __init__(self, name):
        name = f"[{name}]"
        self._name = f"{name:<28}"

    def log(self, level, msg):
        global _print

        if level >= _lvl:
            _print(_lchr[level], self._name, msg)

    def debug(self, msg):
        self.log(DEBUG, msg)

    def info(self, msg):
        self.log(INFO, msg)

    def warning(self, msg):
        self.log(WARNING, msg)

    def error(self, msg):
        self.log(ERROR, msg)

    def critical(self, msg):
        self.log(CRITICAL, msg)


def getLogger(name):
    logger = Logger(name)
    logger.debug("Loading module ...")
    return logger


from config import sys

if sys["verbose_log"] or sys["exception_dump"]:
    try:
        _log = open("sys.log", "a")
    except:
        _log = open("sys.log", "w")

    _log.seek(0, 2)


def dump_exception(msg, exc):
    print(msg)
    print_exception(exc)

    if sys["exception_dump"] > 0:
        pos = _log.tell()

        if pos < sys["exception_dump"]:
            dt = RTC().datetime()
            _log.write(f"\n{dt[2]}.{dt[1]}.{dt[0]} {dt[4]}:{dt[5]:02} :: ")
            _log.write(msg)
            _log.write("\n")
            print_exception(exc, _log)
            _log.flush()


def _print(*args):
    print(*args)

    pos = _log.tell()

    if pos < sys["exception_dump"]:
        dt = RTC().datetime()
        _log.write(f"{dt[2]}.{dt[1]}.{dt[0]} {dt[4]}:{dt[5]:02} ::")

        for s in args:
            _log.write(str(s))

        _log.write("\n")
        _log.flush()


if not sys["verbose_log"]:
    _print = print

_print(f"Loading module {__name__}")
