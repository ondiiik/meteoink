from ulogging import getLogger

logger = getLogger(__name__)

from machine import Pin, ADC
from config import hw, vbat
from utime import sleep_ms
from display.epd import EPD


class Battery:
    def __init__(self):
        self.adc = ADC(Pin(hw["pins"]["vbat"]))
        self.adc.atten(ADC.ATTN_11DB)

    @property
    def voltage(self):
        return self.adc.read() * vbat["adc2volt"]


battery = Battery()
