from ulogging import getLogger

logger = getLogger(__name__)

from machine import Pin, PWM
from config import sys, hw


class Led:
    OFF = 0
    WARM_UP = 1
    DOWNLOAD = 2
    DRAWING = 3
    FLUSHING = 3
    ALERT = 4

    def __init__(self):
        p = hw["pins"]["led"]
        self._pin = PWM(Pin(p), freq=1, duty=0) if p >= 0 else None
        self._enabled = sys["led_enabled"]

    def disable(self):
        if self._pin is not None:
            self._enabled = False
            self._pin.duty(0)
            self._pin.freq(1)

    def mode(self, m):
        if self._pin is not None:
            if self._enabled:
                if m == Led.WARM_UP:
                    self._pin.duty(256)
                    self._pin.freq(400)
                elif m == Led.DOWNLOAD:
                    self._pin.duty(1)
                    self._pin.freq(1)
                elif m == Led.DRAWING:
                    self._pin.duty(4)
                    self._pin.freq(400)
                elif m == Led.FLUSHING:
                    self._pin.duty(1)
                    self._pin.freq(4)
                elif m == Led.ALERT:
                    self._pin.duty(16)
                    self._pin.freq(10)
                else:
                    self._pin.duty(0)
                    self._pin.freq(1)
            else:
                self._pin.duty(0)
                self._pin.freq(1)
