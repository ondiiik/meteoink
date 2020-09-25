def voltage():
    from machine import Pin, ADC
    from config  import pins
    adc = ADC(Pin(pins.VBAT))
    adc.atten(ADC.ATTN_6DB)
    return adc.read() / 833.738


