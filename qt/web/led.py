from config import location
from log    import dump_exception
from lang   import trn


def page(web):
    try:
        loc = location[int(web.args['idx'])]
        yield web.heading( 2, trn['Edit location'])
        yield web.form_head('lset')
        yield web.form_variable('idx',  web.args['idx'])
        yield web.form_input(trn['Location name'], 'name', loc.name)
        yield web.form_input(trn['Latitude'],      'lat',  loc.lat)
        yield web.form_input(trn['Longitude'],     'lon',  loc.lon)
        yield web.form_tail()
    except Exception as e:
        dump_exception('WEB error:', e)
        yield web.index
