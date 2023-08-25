from ulogging import getLogger

logger = getLogger(__name__)

from config import location
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    i = int(args["idx"])
    gps = [
        float(ll[:-1] if ll[-1] in ("N", "E") else ll) for ll in args["gps"].split(",")
    ]
    l = location["locations"][i]
    l["name"] = args["name"]
    l["lat"] = gps[0]
    l["lon"] = gps[1]
    location.flush()

    web.index(page)
