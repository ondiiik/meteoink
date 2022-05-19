from ulogging import getLogger
logger = getLogger(__name__)

from buzzer import play
from machine import reset
from ui import DISPLAY_GREETINGS
from db import display
import web


@web.action_handler(__name__)
def www(page, args):
    play((2093, 30), 120, (1568, 30), 120, (1319, 30), 120, (1047, 30))
    display.DISPLAY_STATE = DISPLAY_GREETINGS
    reset()
