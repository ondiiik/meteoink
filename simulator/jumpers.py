from machine import Pin
from config import pins, connection, location, ui


class Jumpers:
    class PinDummy:
        @staticmethod
        def value():
            return 1

    def __init__(self):
        self._hp = self._init_pin(pins.HOTSPOT_BUTTON)
        self._al = self._init_pin(pins.ALLERT_BUTTON)
        self._sl = self._init_pin(pins.SLEEP_BUTTON)

    def _init_pin(self, pin):
        if 0 > pin:
            return self.PinDummy()
        else:
            return Pin(pin, Pin.IN, Pin.PULL_UP)

    @property
    def hotspot(self):
        return 0 == self._hp.value() or \
            0 == len(connection) or \
            0 == len(location) or \
            '' == ui.apikey

    @property
    def alert(self):
        return 0 == self._al.value()

    @property
    def sleep(self):
        return 0 == self._sl.value()


jumpers = Jumpers()
