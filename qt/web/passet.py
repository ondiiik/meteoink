from config import hotspot
from log    import dump_exception


def page(web):
    try:
        p1 = web.args['p1']
        p2 = web.args['p2']
        
        if p1 == p2:
            hotspot.passwd = p1
            hotspot.flush()
    
    except Exception as e:
        dump_exception('WEB error:', e)
    
    return True
