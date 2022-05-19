from ulogging import getLogger
logger = getLogger(__name__)

from db import time
import web


@web.action_handler(__name__)
def www(page, args):
    time.WINTER = True
    web.index(page)
