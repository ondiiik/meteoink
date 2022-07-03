from config import connection, Connection
from log import dump_exception
from web import bssid2bytes


def page(web):
    try:
        if 'bssid' in web.args:
            bssid = bssid2bytes(web.args['bssid'])
        else:
            bssid = None

        for c in connection:
            if c.bssid == bssid:
                from .set import page
                page(web)
                return

        connection.append(Connection(int(web.args['location']), web.args['ssid'], web.args['psw'], bssid))
        Connection.flush()

    except Exception as e:
        dump_exception('WEB error:', e)

    yield web.index
