from config import hotspot
from log    import dump_exception


def page(web):
    try:
        hotspot.ssid = web.args['id']
        hotspot.flush()
    except Exception as e:
        dump_exception('WEB error:', e)
    
    return True
