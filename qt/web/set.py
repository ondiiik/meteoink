from micropython import const
from config      import connection, flush_connections
from .           import bssid2bytes


_spaces = const(4)


def page(web):
    # Checks if this bssid exists and modify it
    bssid = bssid2bytes(web.args['bssid'])
    
    for i in range(len(connection)):
        if connection[i].bssid == bssid:
            connection[i].passwd   = web.args['psw']
            connection[i].location = web.args['location']
            connection[i].lat      = web.args['lat']
            connection[i].lon      = web.args['lon']
            break
    
    # Write result to configuration
    flush_connections()
    
    from .index import page
    page(web)
