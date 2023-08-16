from ulogging import getLogger

logger = getLogger(__name__)

from buzzer import play
from machine import reset
from ui import DISPLAY_GREETINGS
from config import display
import web


@web.action_handler(__name__)
def www(page, args):
    play((2093, 30), 120, (1568, 30), 120, (1319, 30), 120, (1047, 30))
    display["display_state"] = DISPLAY_GREETINGS
    display.flush()
    reset()
