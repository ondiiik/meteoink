print('Reading database ...')

from machine import reset
from .base import init
from .structs import Location, Connection
from collections import namedtuple
from random import seed, choice

_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

need_reset = False
need_reset |= init('alert', lambda: {'ALREADY_TRIGGERED': False})
need_reset |= init('display', lambda: {'DISPLAY_STATE': 0})
need_reset |= init('led', lambda: {'LED_ENABLED': False})
need_reset |= init('sys', lambda: {'DHT_HUMI_CALIB': (1, 0), 'EXCEPTION_DUMP': 0, 'VERBOSE_LOG': False})
need_reset |= init('beep', lambda: {'TEMP_BALANCED': False, 'ERROR_BEEP': False})
need_reset |= init('location', lambda: {'LOCATIONS': []})
need_reset |= init('connection', lambda: {'CONNECTIONS': []})
need_reset |= init('spot', lambda: {'SSID': 'metoink_' + ''.join([choice(_chars) for _ in range(4)]), 'PASSWD': ''.join([choice(_chars) for _ in range(12)])})
need_reset |= init('temp', lambda: {'INDOOR_HIGH': 26, 'OUTDOOR_HIGH': 27, 'OUTDOOR_LOW': -5})
need_reset |= init('time', lambda: {'WINTER': False})
need_reset |= init('vbat', lambda: {'LOW_VOLTAGE': 3.2, 'SHOW_VOLTAGE': False})
need_reset |= init('api', lambda: {'APIKEY': '', 'UNITS': 'metric', 'LANGUAGE': 'EN', 'VARIANT': 4})
need_reset |= init('ui', lambda: {'REFRESH': 15, 'DBL': (0, 7), 'SHOW_RADAR': 5})

if need_reset:
    reset()
