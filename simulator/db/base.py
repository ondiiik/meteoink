from sys import modules
from .structs import Db


def init(name, items):
    global modules

    try:
        m = __import__(f'db._{name}', None, None, ['object'])
        modules[f'db.{name}'] = m.Data()
        return False
    except BaseException as e:
        write(name, items())
        return True


def write(name, items, cnt=1):
    structures = set()
    for val in items.values():
        if isinstance(val, Db):
            structures.add(type(val))
        elif isinstance(val, list):
            for i in val:
                if isinstance(i, Db):
                    structures.add(type(i))
        elif isinstance(val, dict):
            for i in val.values():
                if isinstance(i, Db):
                    structures.add(type(i))

    with open(f'db/_{name}.py', 'w') as f:
        for s in structures:
            f.write(f'from .structs import {s.__name__}\n')
        f.write(f'''from .base import write

class Data:
    _WRITE_COUNTER = {cnt}

    def __init__(self):
        self._items = {items}

''')

        for item in items:
            f.write(f'''    @property
    def {item}(self):
        return self._items['{item}']

    @{item}.setter
    def {item}(self, value):
        self._items['{item}'] = value
        write('{name}', self._items, self._WRITE_COUNTER + 1)

''')
