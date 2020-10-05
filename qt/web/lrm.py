from config import location, flush_loc


def page(web):
    name = web.args['name']
    
    for i in range(len(location)):
        if location[i].name == name:
            location.remove(location[i])
            break
    
    flush_loc()
    return True
