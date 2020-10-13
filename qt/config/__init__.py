from pyptf       import IS_MICROPYTHON
from micropython import const

VARIANT_2DAYS                 = const(2)
VARIANT_4DAYS                 = const(4)

DISPLAY_REQUIRES_FULL_REFRESH = const(0)
DISPLAY_JUST_REPAINT          = const(1)
DISPLAY_DONT_REFRESH          = const(2)



class Location:
    __slots__ = ('name', 'lat', 'lon')
    
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat  = lat
        self.lon  = lon


class Connection:
    __slots__ = ('ssid', 'bssid', 'passwd', 'location')
    
    def __init__(self, location, ssid, passwd, bssid = None):
        self.ssid     = ssid
        self.bssid    = bssid
        self.passwd   = passwd
        self.location = location


class Spot:
    __slots__   = ('ssid', 'passwd')
    
    def __init__(self, ssid, passwd):
        self.ssid   = ssid
        self.passwd = passwd


class Ui:
    __slots__     = ('apikey', 'units', 'language', 'variant')
    
    def __init__(self, apikey, units, language, variant):
        self.apikey   = apikey
        self.units    = units
        self.language = language
        self.variant  = variant


def flush_con():
    cfg_path = '/config/connection.py'
    
    if not IS_MICROPYTHON:
        cfg_path = '/home/ondiiik/Development/meteo/meteo_py/qt/config/connection.py'
    
    f = open(cfg_path, 'w')
    f.write('from config import Connection\nconnection = [\n')
    
    for c in connection:
        f.write('Connection({}, "{}", "{}", {}),\n'.format(c.location, c.ssid, c.passwd, c.bssid))
    f.write(']')
    f.close()


def flush_loc():
    cfg_path = '/config/location.py'
    
    if not IS_MICROPYTHON:
        cfg_path = '/home/ondiiik/Development/meteo/meteo_py/qt/config/location.py'
    
    f = open(cfg_path, 'w')
    f.write('from config import Location\nlocation = [\n')
    
    for c in location:
        f.write('Location("{}", {}, {}),\n'.format(c.name, c.lat, c.lon))
    f.write(']')
    f.close()


def display_set(val, force = False):
    if force or (not display_get() == val):
        f = open('config/display.py', 'w')
        f.write('DISPLAY_STATE = {}'.format(val))
        f.close()

def display_get():
    try:
        from config import display
        return display.DISPLAY_STATE
    except:
        display_set(DISPLAY_REQUIRES_FULL_REFRESH, True)
        return      DISPLAY_REQUIRES_FULL_REFRESH 


from .connection import connection
from .location   import location
from .spot       import hotspot
from .ui         import ui
