from ulogging import getLogger

logger = getLogger(__name__)

from config import time
import web


@web.action_handler(__name__)
def www(page, args):
    time["winter"] = True
    time.flush()
    web.index(page)
