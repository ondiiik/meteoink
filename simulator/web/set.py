from config import connection
import web


def set(page, args):
    bssid = web.bssid2bytes(args['bssid'])

    for i in range(len(connection)):
        if connection[i].bssid == bssid:
            l = int(args['location']), args['psw']
            connection[i].location, connection[i].passwd = l
            connection[i].flush()
            break

    web.index(page)


@web.webpage_handler(__name__)
def www(page, args):
    set(page, args)
