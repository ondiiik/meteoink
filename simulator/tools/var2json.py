from sys import argv, path
from pathlib import Path
from json import dump


var_path = Path(argv[1])
path.append(str(var_path))
db_path = var_path.joinpath('db')
db_path.mkdir(exist_ok=True)


with db_path.joinpath('structs.py').open('w') as f:
    f.write('''
class Location(dict):
    ...

class Connection(dict):
    def __init__(self, **kw):
        kw["bssid"] = ":".join("{:02X}".format(b) for b in kw["bssid"])
        super().__init__(**kw)
''')


with db_path.joinpath('base.py').open('w') as f:
    f.write('''
class Db(dict):
    def __init__(self, name, data, cnt):
        super().__init__(data)
''')


from _location import Data
_location = Data()
_location['locations'] = _location.pop('LOCATIONS')
with var_path.joinpath('location.json').open('w') as f:
    print('location.json:', _location, '\n')
    dump(_location, f)


from _connection import Data
_connection = Data()
_connection['connections'] = _connection.pop('CONNECTIONS')
with var_path.joinpath('connection.json').open('w') as f:
    print('connection.json:', _connection, '\n')
    dump(_connection, f)

