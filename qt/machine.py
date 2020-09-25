import sys


class SPI:
    def __init__(self, n):
        pass
    
    def init(self, baudrate, polarity, phase, sck, mosi, miso):
        pass

_pins = [1] * 256


_pins[16] = 0 # 1 - Meteostation, 0 - Config server
_pins[23] = 1 # 1 - no alert,     0 - alert


class WDT:
    def __init__(self, timeout):
        pass
    
    def feed(self):
        pass


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


class ADC:
    ATTN_6DB = 1
    
    def __init__(self, pin):
        pass
    
    def atten(self, at):
        pass
    
    def read(self):
        return 3287


class PWM:
    def __init__(self, pin, freq, duty):
        print('BEEP', freq)
    
    def duty(self, v):
        pass
    
    def freq(self, v):
        pass
    
    def deinit(self):
        pass


def freq(max_freq):
    pass


def deepsleep(t):
    print('Deep sleep ....')
    sys.exit()


def reset():
    print('Reset ....')
    sys.exit()


def reset_cause():
    return 0


PWRON_RESET = 1