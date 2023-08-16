from ulogging import getLogger

logger = getLogger(__name__)

from config import vbat
import web


@web.action_handler(__name__)
def www(page, args):
    vbat["low_voltage"] = max(2.8, min(4.0, float(args["v"])))
    web.index(page)
