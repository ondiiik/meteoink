from ulogging import getLogger

logger = getLogger(__name__)

from config import connection
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    bssid = args["bssid"]
    connections = connection["connections"]

    for i in range(len(connections)):
        if connections[i]["bssid"] == bssid:
            connections.remove(connections[i])
            connection.flush()
            break

    web.index(page)
