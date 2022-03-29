from config import connection, Connection
import web


@web.webpage_handler(__name__)
def www(page, args):
    bssid = web.bssid2bytes(args['bssid'])

    for i in range(len(connection)):
        if connection[i].bssid == bssid:
            connection.remove(connection[i])
            Connection.flush()
            break

    web.index(page)
