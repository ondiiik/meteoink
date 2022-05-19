from ulogging import getLogger
logger = getLogger(__name__)

from db import beep
import web


@web.action_handler(__name__)
def www(page, args):
    beep.TEMP_BALANCED = 1
    web.index(page)
