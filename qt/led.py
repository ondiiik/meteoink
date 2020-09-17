class Led():
    OFF      = 0
    WARM_UP  = 1
    DOWNLOAD = 2
    DRAWING  = 3
    FLUSHING = 3
    ALERT    = 4
    
    def __init__(self):
        from machine import Pin, PWM
        from config  import pins
        self._pin = PWM(Pin(pins.LED), freq=1, duty=10)
    
    def mode(self, m):
        if   m == Led.WARM_UP:
            self._pin.duty(256)
            self._pin.freq(400)
        elif m == Led.DOWNLOAD:
            self._pin.duty(8)
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
            self._pin.freq(10)
