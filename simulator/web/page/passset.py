from ulogging import getLogger

logger = getLogger(__name__)

from config import spot
import web


@web.action_handler(__name__)
def www(page, args):
    p = args["p"]
    spot["passwd"] = p
    spot.flush()
    web.index(page)
