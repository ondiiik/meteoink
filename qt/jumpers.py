from machine import Pin
from config  import pins


_hotspot_pin = Pin(pins.HOTSPOT, Pin.IN, Pin.PULL_UP)
_alert_pin   = Pin(pins.ALERT,   Pin.IN, Pin.PULL_UP)


def alert():
    return _alert_pin.value() == 0


def hotspot():
    return _hotspot_pin.value() == 0


def meteostation():
    return not _hotspot_pin.value() == 0
