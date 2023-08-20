from ulogging import getLogger

logger = getLogger(__name__)

from config import hw
from machine import Pin, PWM
from utime import sleep_ms


def play(*pattern):
    p = hw["pins"]["buzzer"]

    if p < 0:
        return

    p = Pin(p)

    for tone in pattern:
        if isinstance(tone, int):
            sleep_ms(tone)
        else:
            beeper = PWM(p, freq=tone[0], duty=512)
            sleep_ms(tone[1])
            beeper.deinit()
