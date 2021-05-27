from machine import deepsleep
from buzzer  import play


def page(web):
    play((2093, 30), 120, (1568, 30), 120, (1319, 30), 120, (1047, 30))
    deepsleep(1)
