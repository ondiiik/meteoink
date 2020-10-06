from config import location, Location, flush_loc


def page(web):
    location.append(Location(web.args['name'], web.args['lat'], web.args['lon']))
    flush_loc()
    return True
