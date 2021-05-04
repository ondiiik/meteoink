from machine import Pin, ADC
from config  import pins


def voltage():
    adc = ADC(Pin(pins.VBAT))
    adc.atten(ADC.ATTN_6DB)
    return adc.read() * 0.0009025

