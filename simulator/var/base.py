from ulogging import getLogger
logger = getLogger(__name__)


from sys import modules


def init(name, items):
    global modules

    try:
        m = __import__(f'var._{name}', None, None, ['object'])
        modules[f'var.{name}'] = m.Data()
        return False
    except BaseException as e:
        write(name, items)
        logger.info(f'Built variables {name}')
        return True


def write(name, items, cnt=1):
    with open(f'var/_{name}.py', 'w') as f:
        f.write(f'''from . import write

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
