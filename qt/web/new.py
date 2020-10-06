from config import connection, Connection, flush_con
from .main  import bssid2bytes


def page(web):
    # Checks if this bssid exists and modify it
    bssid = bssid2bytes(web.args['bssid'])
    
    for c in connection:
        if c.bssid == bssid:
            from .set import page
            page(web)
            return
    
    # Connection is still not there - add new
    connection.append(Connection(int(web.args['location']), web.args['ssid'], web.args['psw'], bssid))
    flush_con()
    
    from .index import page
    page(web)
