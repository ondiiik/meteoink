from config import connection
from log import dump_exception
from web import bssid2bytes


def page(web):
    # Checks if this bssid exists and modify it
    try:
        if 'bssid' in web.args and web.args['bssid']:
            bssid = bssid2bytes(web.args['bssid'])

            for i in range(len(connection)):
                if connection[i].bssid == bssid:
                    l = int(web.args['location']), web.args['psw']
                    connection[i].location, connection[i].passwd = l
                    connection[i].flush()
                    yield web.index
                    return

        ssid = web.args['bssid']

        for i in range(len(connection)):
            if connection[i].ssid == ssid:
                l = int(web.args['location']), web.args['psw']
                connection[i].location, connection[i].passwd = l
                connection[i].flush()
                break

    except Exception as e:
        dump_exception('WEB error:', e)

    # Write result to configuration
    yield web.index
