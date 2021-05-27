from config import connection, Connection
from log    import dump_exception
from web    import bssid2bytes


def page(web):
    try:
        bssid = bssid2bytes(web.args['bssid'])
        
        for i in range(len(connection)):
            if connection[i].bssid == bssid:
                connection.remove(connection[i])
                Connection.flush()
                break
    
    except Exception as e:
        dump_exception('WEB error:', e)
    
    yield web.index
