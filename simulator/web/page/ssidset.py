from ulogging import getLogger

logger = getLogger(__name__)

from config import spot
import web


@web.action_handler(__name__)
def www(page, args):
    spot["ssid"] = args["id"]
    spot.flush()
    web.index(page)
