def led_task(led):
    while led.running:
        led.process()


class Led():
    OFF      = 0
    ON       = 1
    FLASH1   = 2
    FLASH2   = 3
    ALERT    = 4
    
    def __init__(self):
        from machine import Pin
        from _thread import start_new_thread
        self.pin     = Pin(2, Pin.OUT)
        self.running = True
        self._mode   = Led.OFF
        self._code   = ((0, 100),)
        self._idx    = 0
        start_new_thread(led_task, (self,))
    
    def mode(self, m):
        self._idx = 0;
        
        if m == Led.ON:
            self._code = ((1, 100),)
        elif m == Led.FLASH1:
            self._code = ((1, 250), (1, 250), (0, 250), (0, 250))
        elif m == Led.FLASH2:
            self._code = ((1, 50), (0, 50), (1, 50), (0, 250), (0, 250), (0, 250), (0, 250))
        elif m == Led.ALERT:
            self._code = ((1, 30), (0, 30))
        else:
            self._code = ((0, 100),)
    
    
    def process(self):
        from utime import sleep_ms
        
        if self._idx >= len(self._code):
            self._idx = 0
        
        cmd = self._code[self._idx]
        
        if 0 == cmd[0]:
            self.pin.off()
        else:
            self.pin.on()
        
        sleep_ms(cmd[1])
        
        self._idx += 1

