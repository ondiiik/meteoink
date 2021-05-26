from config import location, Location


def page(web):
    location.append(Location(web.args['name'], web.args['lat'], web.args['lon']))
    Location.flush()
    return True
