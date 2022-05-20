from sys import modules
from .structs import DbStruct


class Db:
    def __init__(self, name, items, cnt):
        self._name = name
        self._items = items
        self._cnt = cnt

    def flush(self):
        structures = set()
        for val in self._items.values():
            if isinstance(val, DbStruct):
                structures.add(type(val))
            elif isinstance(val, list):
                for i in val:
                    if isinstance(i, DbStruct):
                        structures.add(type(i))
            elif isinstance(val, dict):
                for i in val.values():
                    if isinstance(i, DbStruct):
                        structures.add(type(i))

        with open(f'db/_{self._name}.py', 'w') as f:
            for s in structures:
                f.write(f'from .structs import {s.__name__}\n')
            f.write(f'''from .base import Db
class Data(Db):
    def __init__(self):
        super().__init__('{self._name}', {self._items}, {self._cnt+1})
''')

    def __getattr__(self, name):
        if name[0] == '_':
            return super().__getattr__(name)

        try:
            return self._items[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name[0] == '_':
            return super().__setattr__(name, value)

        items = self._items
        if name in items:
            items[name] = value
            self.flush()
        else:
            raise AttributeError(name)


def init(name, items):
    global modules

    try:
        m = __import__(f'db._{name}', None, None, ['object'])
        modules[f'db.{name}'] = m.Data()
        return False
    except Exception as font:
        Db(name, items(), 0).flush()
        return True
