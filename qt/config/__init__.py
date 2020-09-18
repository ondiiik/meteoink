from micropython import const

class Connection:
    def __init__(self, location, lat, lon, ssid, passwd, bssid = None):
        __slots__     = ('ssid', 'bssid', 'passwd', 'country', 'location', 'lat', 'lon')
        self.ssid     = ssid
        self.bssid    = bssid
        self.passwd   = passwd
        self.location = location
        self.lat      = lat
        self.lon      = lon


class Spot:
    def __init__(self, ssid, passwd):
        __slots__   = ('ssid', 'passwd')
        self.ssid   = ssid
        self.passwd = passwd


class Ui:
    VARIANT_2DAYS = const(2)
    VARIANT_4DAYS = const(4)
    
    def __init__(self, apikey, units, language, variant):
        __slots__     = ('apikey', 'units', 'language', 'variant')
        self.apikey   = apikey
        self.units    = units
        self.language = language
        self.variant  = variant


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


DISPLAY_REQUIRES_FULL_REFRESH = const(0)
DISPLAY_JUST_REPAINT          = const(1)
DISPLAY_DONT_REFRESH          = const(2)

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


def reset_counter_set(val, force = False):
    if force or (not reset_counter_get() == val):
        f = open('config/resets.py', 'w')
        f.write('RESET_COUNT = {}'.format(val))
        f.close()

def reset_counter_get():
    try:
        from config import resets
        return resets.RESET_COUNT
    except:
        reset_counter_set(0, True)
        return            0 
        


from .connection import connection
from .spot       import hotspot
from .ui         import ui
