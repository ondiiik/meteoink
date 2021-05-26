from config import location


def page(web):
    name = web.args['name']
    
    for i in range(len(location)):
        if location[i].name == name:
            location[i].lat = float(web.args['lat'])
            location[i].lon = float(web.args['lon'])
            location[i].flush()
            break
    
    return True
