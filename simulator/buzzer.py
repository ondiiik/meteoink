from ulogging import getLogger

logger = getLogger(__name__)

from setup import pins
from machine import Pin, PWM
from utime import sleep_ms


def play(*pattern):
    if pins.BUZZER < 0:
        return

    for tone in pattern:
        if isinstance(tone, int):
            sleep_ms(tone)
        else:
            beeper = PWM(Pin(pins.BUZZER), freq=tone[0], duty=512)
            sleep_ms(tone[1])
            beeper.deinit()
