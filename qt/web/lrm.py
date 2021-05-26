from config import location, Location


def page(web):
    name = web.args['name']
    
    for i in range(len(location)):
        if location[i].name == name:
            location.remove(location[i])
            Location.flush()
            break
    
    return True
