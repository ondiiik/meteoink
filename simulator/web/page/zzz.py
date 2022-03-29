from buzzer import play
from machine import reset
from config import DISPLAY_GREETINGS
from var import write
import web


@web.webpage_handler(__name__)
def www(page, args):
    play((2093, 30), 120, (1568, 30), 120, (1319, 30), 120, (1047, 30))
    write('display', (DISPLAY_GREETINGS,))
    reset()
