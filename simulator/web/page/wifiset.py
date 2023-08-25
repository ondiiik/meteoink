import web
from config import connection
from ulogging import getLogger

logger = getLogger(__name__)


def wifiset(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    c = connection["connections"][int(args["idx"])]
    c["ssid"] = args["ssid"]
    c["bssid"] = args["bssid"]
    c["ignore_bssid"] = True if "ib" in args else False
    c["location"] = int(args["location"])
    c["passwd"] = args["psw"]
    connection.flush()

    web.index(page)


@web.action_handler(__name__)
def www(page, args):
    wifiset(page, args)
