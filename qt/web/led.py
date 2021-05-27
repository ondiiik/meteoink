from config import location
from log    import dump_exception


def page(web):
    try:
        loc = location[int(web.args['idx'])]
        yield web.heading( 2, 'Edit location')
        yield web.form_head('lset')
        yield web.form_input('Location name', 'name', loc.name)
        yield web.form_input('Latitude',      'lat',  loc.lat)
        yield web.form_input('Longitude',     'lon',  loc.lon)
        yield web.form_tail()
    except Exception as e:
        dump_exception('WEB error:', e)
        yield web.index
