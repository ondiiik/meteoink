from ulogging import getLogger

logger = getLogger(__name__)

from db import temp
import web


@web.action_handler(__name__)
def www(page, args):
    l = float(args["ihi"]), float(args["ohi"]), float(args["olo"])
    temp.INDOOR_HIGH, temp.OUTDOOR_HIGH, temp.OUTDOOR_LOW = l
    web.index(page)
