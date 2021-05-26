from machine import Pin
from config  import pins, connection, location, ui


class Jumpers:
    class PinDummy:
        @staticmethod
        def value():
            return 1
    
    def __init__(self):
        if 0 > pins.HOTSPOT_BUTTON:
            self._hp = self.PinDummy()
        else:
            self._hp = Pin(pins.HOTSPOT_BUTTON, Pin.IN, Pin.PULL_UP)
    
        if 0 > pins.ALLERT_BUTTON:
            self._al = self.PinDummy()
        else:
            self._al = Pin(pins.ALLERT_BUTTON, Pin.IN, Pin.PULL_UP)
    
    
    @property
    def hotspot(self):
        return 0  == self._hp.value() or \
               0  == len(connection)  or \
               0  == len(location)    or \
               '' == ui.apikey
    
    
    @property
    def alert(self):
        return 0  == self._al.value()


jumpers = Jumpers()