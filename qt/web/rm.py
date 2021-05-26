from config import connection, Connection
from .main  import bssid2bytes


def page(web):
    # Checks if this bssid exists and modify it
    bssid = bssid2bytes(web.args['bssid'])
    
    for i in range(len(connection)):
        if connection[i].bssid == bssid:
            connection.remove(connection[i])
            Connection.flush()
            break
    
    return True
