from config import connection, Connection
import web


@web.webpage_handler(__name__)
def www(page, args):
    bssid = web.bssid2bytes(args['bssid'])

    for c in connection:
        if c.bssid == bssid:
            web.wifiset(page, args)
            return

    connection.append(Connection(int(args['location']), args['ssid'], args['psw'], bssid))
    Connection.flush()

    web.index(page)
