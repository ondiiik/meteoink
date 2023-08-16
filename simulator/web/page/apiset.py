from ulogging import getLogger

logger = getLogger(__name__)

from config import api
import web


@web.action_handler(__name__)
def www(page, args):
    api["apikey"] = args["key"]
    api.flush()
    web.index(page)
