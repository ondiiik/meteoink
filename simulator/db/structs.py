class Db:
    def __init__(self, *args, **kwargs):
        used = set()

        for key, val in zip(self.__slots__, args):
            setattr(self, key, val)
            used.add(key)

        for key, val in kwargs.items():
            if key not in self.__slots__:
                raise RuntimeError(f'Unexpected keyword argument {key}. Available are {", ".join(args)}.')
            setattr(self, key, val)
            used.add(key)

        if len(used) != len(self.__slots__):
            raise RuntimeError(f'Some expected arguments from {", ".join(args)} are missing.')

    def __repr__(self):
        name = type(self).__name__
        vars = {slot: getattr(self, slot) for slot in self.__slots__}
        items = [f'{key}={repr(val)}' for key, val in vars.items()]
        return f'{name}({", ".join(items)})'


class Location(Db):
    __slots__ = 'name', 'lat', 'lon'


class Connection(Db):
    __slots__ = 'location', 'ssid', 'passwd', 'bssid'
