import time
import datetime
import pygame


class SPI:
    def __init__(self, n):
        ...

    def init(self, baudrate, polarity, phase, sck, mosi, miso):
        ...


_pins = [1] * 256


_pins[32] = 1  # 1 - Meteostation, 0 - Config server


class WDT:
    def __init__(self, timeout):
        ...

    def feed(self):
        ...


class Pin:
    OUT = 1
    IN = 2
    PULL_UP = 3
    PULL_DOWN = 4

    def __init__(self, n, t=OUT, p=None):
        self.n = n

    def on(self):
        # print(f'PIN {self.n} ON')
        ...

    def off(self):
        # print(f'PIN {self.n} OFF')
        ...

    def value(self):
        print(f"PIN {self.n} {_pins[self.n]}")
        return _pins[self.n]


class ADC:
    ATTN_6DB = 1
    ATTN_11DB = 2

    def __init__(self, pin):
        ...

    def atten(self, at):
        ...

    def read(self):
        # return 1287
        return 3287


class PWM:
    def __init__(self, pin, freq, duty):
        print("BEEP", freq)

    def duty(self, v):
        ...

    def freq(self, v):
        ...

    def deinit(self):
        ...


class RTC:
    def __init__(self):
        ...

    def datetime(self):
        dt = datetime.datetime.now().timetuple()
        return (
            dt.tm_year,
            dt.tm_mon,
            dt.tm_mday,
            dt.tm_wday,
            dt.tm_hour,
            dt.tm_min,
            dt.tm_sec,
            dt.tm_yday,
        )

    def init(self, v):
        ...


def freq(max_freq):
    ...


_reset_cause = ""


def deepsleep(t=0):
    global _reset_cause
    print("deepsleep", _reset_cause)

    print("Deep sleep ....", t)

    with open("reset_cause.txt", "w") as f:
        if not _reset_cause:
            _reset_cause = "deepsleep"
        f.write(_reset_cause)

    # for i in range(t // 1000):
    while True:
        _check_events()
        time.sleep(1)

    raise MeteoDeepSleep()


def reset():
    global _reset_cause
    print("reset", _reset_cause)

    print("Reset ....")

    with open("reset_cause.txt", "w") as f:
        if not _reset_cause:
            _reset_cause = "reset"
        f.write(_reset_cause)

    raise MeteoRestart()


def _power_on():
    global _reset_cause
    print("_power_on", _reset_cause)

    print("Power ON ....")

    with open("reset_cause.txt", "w") as f:
        f.write("power_on")

    raise MeteoPowerOn()


SOFT_RESET = 5
HARD_RESET = 2
PWRON_RESET = 1
DEEPSLEEP = 4


def reset_cause():
    try:
        with open("reset_cause.txt", "r") as f:
            v = f.read()
            if v == "deepsleep":
                return DEEPSLEEP
            elif v == "reset":
                return HARD_RESET
            else:
                return PWRON_RESET
    except:
        return PWRON_RESET


def _check_events():
    global _adc

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Bye bye ...")
            _power_on()

        else:
            print("EVENT:", event)


def unique_id():
    return b"12345678987654321"


class MeteoDeepSleep(SystemExit):
    ...


class MeteoRestart(SystemExit):
    ...


class MeteoPowerOn(SystemExit):
    ...
