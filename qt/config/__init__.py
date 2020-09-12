class Connection:
    def __init__(self, country, location, ssid, passwd, bssid = None):
        __slots__     = ('ssid', 'bssid', 'passwd', 'country', 'location')
        self.ssid     = ssid
        self.bssid    = bssid
        self.passwd   = passwd
        self.country  = country
        self.location = location


class Spot:
    def __init__(self, ssid, passwd):
        __slots__   = ('ssid', 'passwd')
        self.ssid   = ssid
        self.passwd = passwd


class Ui:
    def __init__(self, apikey, units, language):
        __slots__     = ('apikey', 'units', 'language')
        self.apikey   = apikey
        self.units    = units
        self.language = language


def flush_connections():
    from sys import implementation
    
    cfg_path = '/config/connection.py'
    
    if not implementation.name == 'micropython':
        cfg_path = '/home/ondiiik/Development/meteo/meteo_ink/meteo_ink/pyPc/config/connection.py'
    
    f = open(cfg_path, 'w')
    f.write('from config import Connection\nconnection = [\n')
    
    for c in connection:
        f.write('Connection("{}", "{}", "{}", "{}", {}),\n'.format(c.country, c.location, c.ssid, c.passwd, c.bssid))
    f.write(']')
    f.close()


from .connection import connection
from .spot       import hotspot
from .ui         import ui
