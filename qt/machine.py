class SPI:
    def __init__(self, n):
        pass
    
    def init(self, baudrate, polarity, phase, sck, mosi, miso):
        pass

_pins = [1] * 256


_pins[16] = 1


class Pin:
    OUT       = 1
    IN        = 2
    PULL_UP   = 3
    PULL_DOWN = 4
    
    def __init__(self, n, t = OUT, p = None):
        self.n = n
    
    def on(self):
        #print('PIN {} ON'.format(self.n))
        pass
    
    def off(self):
        #print('PIN {} OFF'.format(self.n))
        pass
    
    def value(self):
        print('PIN {} {}'.format(self.n, _pins[self.n]))
        return _pins[self.n]


def deepsleep(t):
    pass


def reset():
    pass