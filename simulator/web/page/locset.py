from ulogging import getLogger

logger = getLogger(__name__)

from db import location
import web


@web.action_handler(__name__)
def www(page, args):
    i = int(args["idx"])
    gps = [
        float(ll[:-1] if ll[-1] in ("N", "E") else ll) for ll in args["gps"].split(",")
    ]
    location = location.LOCATIONS[i]
    location.name = args["name"]
    location.lat = gps[0]
    location.lon = gps[1]
    location.flush()

    web.index(page)
