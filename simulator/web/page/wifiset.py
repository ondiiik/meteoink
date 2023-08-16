import web
from config import connection
from ulogging import getLogger

logger = getLogger(__name__)


def wifiset(page, args):
    for i in range(len(connection["connections"])):
        if connection["connections"][i]["bssid"] == bssid:
            if "location" in args:
                connection["connections"][i]["location"] = int(args["location"])
            connection["connections"][i].passwd = args["psw"]
            connection.flush()
            break

    web.index(page)


@web.action_handler(__name__)
def www(page, args):
    wifiset(page, args)
