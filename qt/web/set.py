from config import connection, flush_con
from .main  import bssid2bytes


def page(web):
    # Checks if this bssid exists and modify it
    bssid = bssid2bytes(web.args['bssid'])
    
    for i in range(len(connection)):
        if connection[i].bssid == bssid:
            connection[i].passwd   = web.args['psw']
            connection[i].location = int(web.args['location'])
            break
    
    # Write result to configuration
    flush_con()
    return True
