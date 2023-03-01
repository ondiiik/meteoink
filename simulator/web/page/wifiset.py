import web
from db import connection
from ulogging import getLogger
logger = getLogger(__name__)


def wifiset(page, args):
    bssid = web.bssid2bytes(args['bssid'])

    for i in range(len(connection.CONNECTIONS)):
        if connection.CONNECTIONS[i].bssid == bssid:
            if 'location' in args:
                connection.CONNECTIONS[i].location = int(args['location'])
            connection.CONNECTIONS[i].passwd = args['psw']
            connection.flush()
            break

    web.index(page)


@web.action_handler(__name__)
def www(page, args):
    wifiset(page, args)
