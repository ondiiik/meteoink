from ulogging import getLogger
logger = getLogger(__name__)

from db import connection, Connection
import web


@web.action_handler(__name__)
def www(page, args):
    bssid = web.bssid2bytes(args['bssid'])
    connections = connection.CONNECTIONS

    for c in connections:
        if c.bssid == bssid:
            web.wifiset(page, args)
            return

    connections.append(Connection(int(args['location']), args['ssid'], args['psw'], bssid))
    connection.CONNECTIONS = connections

    web.index(page)
