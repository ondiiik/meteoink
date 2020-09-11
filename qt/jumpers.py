from machine import Pin
from config  import pins


_hotspot_pin = Pin(pins.HOTSPOT, Pin.IN, Pin.PULL_UP)


def hotspot():
    return _hotspot_pin.value() == 0


def meteostation():
    return not _hotspot_pin.value() == 0
