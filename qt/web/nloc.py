from config import location, Location
from log    import dump_exception


def page(web):
    try:
        location.append(Location(web.args['name'], web.args['lat'], web.args['lon']))
        Location.flush()
    except Exception as e:
        dump_exception('WEB error:', e)
    
    return True
