from config import location
from log    import dump_exception


def page(web):
    try:
        pg  = web.heading( 2, 'Edit location')
        loc = location[int(web.args['idx'])]
    
        pg += web.form_head('lset')
        pg += web.form_input('Location name', 'name', loc.name)
        pg += web.form_input('Latitude',      'lat',  loc.lat)
        pg += web.form_input('Longitude',     'lon',  loc.lon)
        pg += web.form_tail()
    except Exception as e:
        dump_exception('WEB error:', e)
    
    web.write(pg)
