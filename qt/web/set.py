from config import connection
from .main  import bssid2bytes
from log    import dump_exception


def page(web):
    # Checks if this bssid exists and modify it
    try:
        bssid = bssid2bytes(web.args['bssid'])
        
        for i in range(len(connection)):
            if connection[i].bssid == bssid:
                l = int(web.args['location']), web.args['psw']
                connection[i].location, connection[i].passwd = l
                connection[i].flush()
                break
    
    except Exception as e:
        dump_exception('WEB error:', e)
    
    # Write result to configuration
    return True
