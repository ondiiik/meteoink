from ulogging import getLogger

logger = getLogger(__name__)

from config import location
import web


@web.action_handler(__name__)
def www(page, args):
    gps = [
        float(ll[:-1] if ll[-1] in ("N", "E") else ll) for ll in args["gps"].split(",")
    ]
    locations = location["locations"]
    locations.append({"name": args["name"], "lat": gps[0], "lon": gps[1]})
    location.flush()

    web.index(page)
