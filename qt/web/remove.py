from micropython import const
from config      import connection, flush_connections
from .           import bssid2bytes


_spaces = const(4)


def page(web):
    # Checks if this bssid exists and modify it
    bssid = bssid2bytes(web.args['bssid'])
    
    for i in range(len(connection)):
        if connection[i].bssid == bssid:
            connection.remove(connection[i])
            break
    
    # Write result to configuration
    flush_connections()
    
    from .index import page
    page(web)
