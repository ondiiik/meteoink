def voltage():
    from machine import Pin, ADC
    from config  import pins
    adc = ADC(Pin(pins.VBAT))
    adc.atten(ADC.ATTN_6DB)
    adc = adc.read()
    
    if adc >= 4095:
        return 4.2
    
    return adc / 1023.75


