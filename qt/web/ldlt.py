from config import location
from log    import dump_exception


def page(web):
    try:
        pg  = web.heading( 2, 'DELETE LOCATION ??!')
        loc = location[int(web.args['idx'])]
    
        yield web.form_head('lrm')
        yield web.form_label('Name',      'name', loc.name)
        yield web.form_label('Latitude',  'lat',  loc.lat)
        yield web.form_label('Longitude', 'lon',  loc.lon)
        yield web.form_tail()
    except Exception as e:
        dump_exception('WEB error:', e)
        yield web.index