from machine import Pin
from config  import pins, connection, location, ui


class Jumpers:
    class PinDummy:
        @staticmethod
        def value():
            return 1
    
    
    def __init__(self):
        self.refresh = self._init_pin( pins.REFRESH_BUTTON ).value() == 0
        self.alert   = self._init_pin( pins.ALLERT_BUTTON  ).value() == 0
        self.sleep   = self._init_pin( pins.SLEEP_BUTTON   ).value() == 0
        self._hp     = self._init_pin( pins.HOTSPOT_BUTTON ).value() == 0
    
    
    def _init_pin(self, pin):
        if 0 > pin:
            return self.PinDummy()
        else:
            return Pin(pin, Pin.IN, Pin.PULL_UP)
    
    
    @property
    def hotspot(self):
        return self._hp or 0 == len(connection) or 0 == len(location) or '' == ui.apikey


jumpers = Jumpers()