import sys
import time
import datetime
import pygame


class SPI:
    def __init__(self, n):
        pass
    
    def init(self, baudrate, polarity, phase, sck, mosi, miso):
        pass

_pins = [1] * 256


_pins[32] = 0 # 1 - Meteostation, 0 - Config server


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
    ATTN_11DB = 2
    
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


class RTC():
    def __init__(self):
        pass
    
    def datetime(self):
        dt = datetime.datetime.now().timetuple()
        return dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_wday, dt.tm_hour, dt.tm_min, dt.tm_sec, dt.tm_yday 
    
    def init(self, v):
        pass

def freq(max_freq):
    pass


def deepsleep(t = 0):
    print('Deep sleep ....')
    for i in range(t // 1000):
        _check_events()
        time.sleep(1)
    sys.exit(0)


def reset():
    print('Reset ....')
    sys.exit()


def reset_cause():
    return 0


DEEPSLEEP = 0


def _check_events():
    global _adc
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Bye bye ...')
            sys.exit(0)
         
        else:
            print('EVENT:', event)


PWRON_RESET = 1