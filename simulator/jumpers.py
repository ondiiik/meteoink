from ulogging import getLogger
logger = getLogger(__name__)

from machine import Pin, reset_cause, DEEPSLEEP
from setup import pins
from buzzer import play


def _pin_value(pin):
    if 0 > pin:
        return False
    else:
        p = Pin(pin, Pin.IN, Pin.PULL_UP)
        return not p.value()


class jumpers:
    hotspot = _pin_value(pins.HOTSPOT_BUTTON)
    alert = _pin_value(pins.ALLERT_BUTTON)
    sleep = _pin_value(pins.SLEEP_BUTTON)


if not DEEPSLEEP == reset_cause():
    play((2093, 30))
