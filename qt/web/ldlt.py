from config import location
from log    import dump_exception


def page(web):
    try:
        pg  = web.heading( 2, 'DELETE LOCATION ??!')
        loc = location[int(web.args['idx'])]
    
        pg += web.form_head('lrm')
        pg += web.form_label('Name',      'name', loc.name)
        pg += web.form_label('Latitude',  'lat',  loc.lat)
        pg += web.form_label('Longitude', 'lon',  loc.lon)
        pg += web.form_tail()
    except Exception as e:
        dump_exception('WEB error:', e)
    
    web.write(pg)
