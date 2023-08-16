from ulogging import getLogger

logger = getLogger(__name__)

from config import beep
import web


@web.action_handler(__name__)
def www(page, args):
    beep["error_beep"] = 0
    beep.flush()
    web.index(page)
