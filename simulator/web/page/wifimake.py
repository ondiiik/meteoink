from ulogging import getLogger

logger = getLogger(__name__)

from config import connection
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    bssid = args["bssid"]
    connections = connection["connections"]

    for c in connections:
        if c["bssid"] == bssid:
            args["idx"] = str(connections.index(c))
            web.wifiset(page, args)
            return

    connections.append(
        {
            "location": int(args["location"]),
            "ssid": args["ssid"],
            "bssid": bssid,
            "passwd": args["psw"],
        }
    )
    connection["connections"] = connections
    connection.flush()

    web.index(page)
