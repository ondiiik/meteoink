from config import location, flush_loc


def page(web):
    name = web.args['name']
    
    for i in range(len(location)):
        if location[i].name == name:
            location[i].lat = float(web.args['lat'])
            location[i].lon = float(web.args['lon'])
            break
    
    flush_loc()
    return True
