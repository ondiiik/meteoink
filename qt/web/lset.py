from config import location
from log    import dump_exception


def page(web):
    try:
        name = web.args['name']
        
        for i in range(len(location)):
            if location[i].name == name:
                l = float(web.args['lat']), float(web.args['lon'])
                location[i].lat, location[i].lon = l
                location[i].flush()
                
                break
    
    except Exception as e:
        dump_exception('WEB error:', e)
    
    return True
