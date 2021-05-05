from machine import Pin
from config  import pins


class Jumpers:
    def __init__(self):
        self._hp = Pin(pins.HOTSPOT, Pin.IN, Pin.PULL_UP)
    
    @property
    def hotspot(self):
        return self._hp.value() == 0


jumpers = Jumpers()