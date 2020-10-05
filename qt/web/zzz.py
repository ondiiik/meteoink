from buzzer  import play
from machine import deepsleep


def page(web):
    play(((2093, 30), (0, 120), (1568, 30), (0, 120), (1319, 30), (0, 120), (1047, 30)))
    deepsleep()