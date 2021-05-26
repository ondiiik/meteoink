from config import hotspot


def page(web):
    p1 = web.args['p1']
    p2 = web.args['p2']
    
    if p1 == p2:
        hotspot.passwd = p1
        hotspot.flush()
    
    return True
