from ulogging import getLogger

logger = getLogger(__name__)

from machine import Pin, reset_cause, PWRON_RESET
from config import hw
from buzzer import play


def _pin_value(pin):
    if 0 > pin:
        return False
    else:
        p = Pin(pin, Pin.IN, Pin.PULL_UP)
        return not p.value()


class jumpers:
    b = hw["buttons"]
    hotspot = _pin_value(b["hotspot"])
    alert = _pin_value(b["alert"])
    sleep = _pin_value(b["sleep"])


if PWRON_RESET == reset_cause():
    play((2093, 30))
