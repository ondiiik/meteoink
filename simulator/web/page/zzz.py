from ulogging import getLogger

logger = getLogger(__name__)

from buzzer import play
from machine import reset
from config import display
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    play((2093, 30), 120, (1568, 30), 120, (1319, 30), 120, (1047, 30))
    display["greetings"] = True
    display.flush()
    reset()
