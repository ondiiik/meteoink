from micropython import const
from config      import location, flush_loc


_spaces = const(4)


def page(web):
    name = web.args['name']
    
    for i in range(len(location)):
        if location[i].name == name:
            location[i].lat = float(web.args['lat'])
            location[i].lon = float(web.args['lon'])
            break
    
    flush_loc()
    return True
