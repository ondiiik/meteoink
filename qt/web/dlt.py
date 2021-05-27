from config import connection, location
from log    import dump_exception
from web    import bytes2bssid


def page(web):
    try:
        yield web.heading( 2, 'DELETE CONNECTION ??!')
        config = connection[int(web.args['idx'])]
        
        yield web.form_head('rm')
        yield web.form_label('SSID',     'ssid',  config.ssid)
        yield web.form_label('BSSID',    'bssid', bytes2bssid(config.bssid))
        yield web.form_spacer()
        yield web.form_label('Location', 'loc',   location[config.location].name)
        yield web.form_tail()
        
    except Exception as e:
        dump_exception('WEB error:', e)
        yield web.index
