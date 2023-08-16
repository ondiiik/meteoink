from ulogging import getLogger

logger = getLogger(__name__)

from config import temp
import web


@web.action_handler(__name__)
def www(page, args):
    l = float(args["ihi"]), float(args["ohi"]), float(args["olo"])
    temp["indoor_high"], temp["outdoor_high"], temp["outdoor_low"] = l
    temp.flush()
    web.index(page)
