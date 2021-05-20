from machine import Pin, ADC
from config  import pins


class Battery:
    @property
    def voltage(self):
        adc = ADC(Pin(pins.VBAT))
        adc.atten(ADC.ATTN_11DB)
        return adc.read() * 0.001706822


battery = Battery()
