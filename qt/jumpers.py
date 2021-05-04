from machine import Pin
from config  import pins


_hotspot_pin = Pin(pins.HOTSPOT, Pin.IN, Pin.PULL_UP)


def __getattr__(name):
    if name == 'hotspot':
        return _hotspot_pin.value() == 0
    raise AttributeError("module '{}' has no attribute '{}'".format(__name__, name))
