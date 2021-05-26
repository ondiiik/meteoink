from collections import namedtuple

def print_exception(e):
    raise e

Implementation = namedtuple('Implementation', ('name', 'version', 'mpy'))
implementation = Implementation('pc', (1, 15, 0), 10757)