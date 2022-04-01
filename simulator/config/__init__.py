from micropython import const
from machine import reset


VARIANT_2DAYS = const(2)
VARIANT_4DAYS = const(4)

DISPLAY_GREETINGS = const(-1)
DISPLAY_REQUIRES_FULL_REFRESH = const(0)
DISPLAY_JUST_REPAINT = const(1)
DISPLAY_DONT_REFRESH = const(2)

DISPLAY_REFRESH_DIV = const(2)


class Location:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

    @staticmethod
    def flush():
        try:
            from config import location
        except:
            location = []

        try:
            from config.connection import _cnt
        except:
            _cnt = 0

        _cnt += 1
        with open('config/location.py', 'w') as f:
            f.write('from config import Location\nlocation = [\n')

            for c in location:
                f.write(f'Location("{c.name}", {c.lat}, {c.lon}),\n')

            f.write(f']\n\n_cnt = {_cnt}')


class Connection:
    def __init__(self, location, ssid, passwd, bssid=None):
        self.ssid = ssid
        self.bssid = bssid
        self.passwd = passwd
        self.location = location

    @staticmethod
    def flush():
        try:
            from config import connection
        except:
            connection = []

        try:
            from config.connection import _cnt
        except:
            _cnt = 0

        _cnt += 1
        with open('config/connection.py', 'w') as f:
            f.write('from config import Connection\nconnection = [\n')

            for c in connection:
                f.write(f'Connection({c.location}, "{c.ssid}", "{c.passwd}", {c.bssid}),\n')

            f.write(f']\n\n_cnt = {_cnt}')


class Spot:
    def __init__(self, ssid, passwd):
        self.ssid = ssid
        self.passwd = passwd

    def flush(self):
        try:
            from config.spot import _cnt
        except:
            _cnt = 0

        _cnt += 1
        with open('config/spot.py', 'w') as f:
            f.write(f'''from config import Spot
hotspot = Spot('{self.ssid}', '{self.passwd}')

_cnt = {_cnt}
''')


class Ui:
    def __init__(self, apikey, units, language, variant, refresh, dbl_refr_range):
        self.apikey = apikey
        self.units = units
        self.language = language
        self.variant = variant
        self.refresh = refresh
        self.dbl = dbl_refr_range

    @property
    def variant_string(self):
        return 'Two days' if self.variant == VARIANT_2DAYS else 'Four days'

    def flush(self):
        try:
            from config.ui import _cnt
        except:
            _cnt = 0

        _cnt += 1
        with open('config/ui.py', 'w') as f:
            v = 'VARIANT_4DAYS' if self.variant == VARIANT_4DAYS else 'VARIANT_2DAYS'
            f.write(f'''from config import Ui, {v}
ui = Ui("{self.apikey}", "{self.units}", "{self.language}", {v}, {self.refresh}, {self.dbl})

_cnt = {_cnt}
''')


class Alert:
    def __init__(self, temp_balanced, error_beep):
        self.temp_balanced = temp_balanced
        self.error_beep = error_beep

    def flush(self):
        try:
            from config.alert import _cnt
        except:
            _cnt = 0

        _cnt += 1
        with open('config/alert.py', 'w') as f:
            f.write(f'''from config import Alert
alert = Alert({self.temp_balanced}, {self.error_beep})

_cnt = {_cnt}
''')


class VBat:
    def __init__(self, low_voltage, show_voltage):
        self.low_voltage = low_voltage
        self.show_voltage = show_voltage

    def flush(self):
        try:
            from config.vbat import _cnt
        except:
            _cnt = 0

        _cnt += 1
        with open('config/vbat.py', 'w') as f:
            f.write(f'''from config import VBat
vbat = VBat({self.low_voltage}, {self.show_voltage})

_cnt = {_cnt}
''')


class Temp:
    def __init__(self, indoor_high, outdoor_high, outdoor_low):
        self.indoor_high = indoor_high
        self.outdoor_high = outdoor_high
        self.outdoor_low = outdoor_low

    def flush(self):
        try:
            from config.vbat import _cnt
        except:
            _cnt = 0

        _cnt += 1
        with open('config/temp.py', 'w') as f:
            f.write(f'''from config import Temp
temp = Temp({self.indoor_high}, {self.outdoor_high}, {self.outdoor_low})

_cnt = {_cnt}
''')


def _rebuild(name, tp, *args):
    print('Rebuildng config for', name)
    i = tp(*args)
    i.flush()
    return True


reload = False

try:
    from .connection import connection
except:
    reload = _rebuild('connection', Connection, None, None, None) or reload

try:
    from .location import location
except:
    reload = _rebuild('location', Location, None, None, None) or reload

try:
    from .spot import hotspot
except:
    from random import seed, choice
    from esp32 import raw_temperature
    seed(raw_temperature())
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    reload = _rebuild('hotspot',
                      Spot,
                      'metoink_' + ''.join([choice(chars) for x in range(4)]),
                      ''.join([choice(chars) for x in range(12)])) or reload

try:
    from .ui import ui
except:
    reload = _rebuild('ui', Ui, "", "metric", "EN", VARIANT_4DAYS, 20, (0, 7)) or reload

try:
    from .alert import alert
except:
    reload = _rebuild('alert', Alert, False, False) or reload

try:
    from .vbat import vbat
except:
    reload = _rebuild('vbat', VBat, 3.2, False) or reload

try:
    from .temp import temp
except:
    reload = _rebuild('temp', Temp, 26.0, 27.0, -5.0) or reload


if reload:
    print('Configuration rebuilt - restart required')
    reset()
