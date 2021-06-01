from config import hotspot
from log    import dump_exception


def page(web):
    try:
        p = web.args['p']
        hotspot.passwd = p
        hotspot.flush()
    
    except Exception as e:
        dump_exception('WEB error:', e)
    
    yield web.index
