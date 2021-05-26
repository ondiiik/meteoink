from buzzer  import play
from machine import reset
from config  import display_set, DISPLAY_GREETINGS


def page(web):
    play((2093, 30), 120, (1568, 30), 120, (1319, 30), 120, (1047, 30))
    display_set(DISPLAY_GREETINGS)
    reset()