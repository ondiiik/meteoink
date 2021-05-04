from config  import pins
from machine import Pin, PWM
from utime   import sleep_ms
    

def play(pattern):
    for tone in pattern:
        if tone[0] == 0:
            sleep_ms(tone[1])
        else:
            beeper = PWM(Pin(pins.BUZZER), freq=tone[0], duty=512)
            sleep_ms(tone[1])
            beeper.deinit()