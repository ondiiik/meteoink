from config import connection, flush_con
from .main  import bssid2bytes


def page(web):
    # Checks if this bssid exists and modify it
    bssid = bssid2bytes(web.args['bssid'])
    
    for i in range(len(connection)):
        if connection[i].bssid == bssid:
            connection[i].passwd   = web.args['psw']
            connection[i].location = int(web.args['location'])
            connection[i].flush()
            break
    
    # Write result to configuration
    return True
