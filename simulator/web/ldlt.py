from config import location
from log    import dump_exception
from lang   import trn


def page(web):
    try:
        yield web.heading(2, trn['DELETE LOCATION'] + ' ??!')
        loc = location[int(web.args['idx'])]
    
        yield web.form_head('lrm')
        yield web.form_label(trn['Name'],      'name', loc.name)
        yield web.form_label(trn['Latitude'],  'lat',  loc.lat)
        yield web.form_label(trn['Longitude'], 'lon',  loc.lon)
        yield web.form_tail()
    except Exception as e:
        dump_exception('WEB error:', e)
        yield web.index