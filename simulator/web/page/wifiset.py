from config import connection
import web


def wifiset(page, args):
    bssid = web.bssid2bytes(args['bssid'])

    for i in range(len(connection)):
        if connection[i].bssid == bssid:
            if 'location' in args:
                connection[i].location = int(args['location'])
            connection[i].passwd = args['psw']
            connection[i].flush()
            break

    web.index(page)


@web.webpage_handler(__name__)
def www(page, args):
    wifiset(page, args)
