from ulogging import getLogger

logger = getLogger(__name__)

from config import api
import web


@web.action_handler(__name__)
def www(page, args):
    api["variant"] = int(args["v"])
    web.index(page)
