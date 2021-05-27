from config import location, Location
from log    import dump_exception


def page(web):
    try:
        name = web.args['name']
        
        for i in range(len(location)):
            if location[i].name == name:
                location.remove(location[i])
                Location.flush()
                break
        
    except Exception as e:
        dump_exception('WEB error:', e)
    
    return True
