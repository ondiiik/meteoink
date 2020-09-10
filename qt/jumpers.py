from machine import Pin

_hotspot_pin = Pin(16, Pin.IN, Pin.PULL_UP)
_ftp_pin     = Pin(17, Pin.IN, Pin.PULL_UP)

def hotspot():
    return _hotspot_pin.value() == 0


def meteostation():
    return (not (_hotspot_pin.value() == 0)) and (not (_ftp_pin.value() == 0))
