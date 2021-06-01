from machine import Pin, ADC
from config  import pins


class Battery:
    def __init__(self):
        self.adc = ADC(Pin(pins.VBAT))
        self.adc.atten(ADC.ATTN_11DB)
    
    @property
    def voltage(self):
        return self.adc.read() * 0.001757813


battery = Battery()
