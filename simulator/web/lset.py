from config import location
from log    import dump_exception


def page(web):
    try:
        i    = int(web.args['idx']) 
        args = web.args['name'], float(web.args['lat']), float(web.args['lon'])
        location[i].name, location[i].lat, location[i].lon = args
        location[i].flush()
    except Exception as e:
        dump_exception('WEB error:', e)
    
    yield web.index
