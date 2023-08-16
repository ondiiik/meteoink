from collections import namedtuple
import traceback


def print_exception(exc):
    traceback.print_exc()


Implementation = namedtuple("Implementation", ("name", "version", "mpy"))
implementation = Implementation("pc", (1, 15, 0), 10757)
