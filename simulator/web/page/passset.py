from ulogging import getLogger

logger = getLogger(__name__)

from db import spot
import web


@web.action_handler(__name__)
def www(page, args):
    p = args["p"]
    spot.PASSWD = p
    web.index(page)
