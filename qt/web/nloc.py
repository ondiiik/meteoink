from micropython import const
from config      import location, Location, flush_loc


_spaces = const(4)


def page(web):
    location.append(Location(web.args['name'], web.args['lat'], web.args['lon']))
    flush_loc()
    
    from .index import page
    page(web)
