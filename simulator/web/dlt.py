from config import connection, location
from log    import dump_exception
from web    import bytes2bssid
from lang   import trn


def page(web):
    try:
        yield web.heading( 2, trn['DELETE CONNECTION'] + ' ??!')
        config = connection[int(web.args['idx'])]
        
        yield web.form_head('rm')
        yield web.form_label('SSID',     'ssid',  config.ssid)
        yield web.form_label('BSSID',    'bssid', bytes2bssid(config.bssid))
        yield web.form_spacer()
        yield web.form_label(trn['Location'], 'loc', location[config.location].name if config.location < len(location) else '...')
        yield web.form_tail()
        
    except Exception as e:
        dump_exception('WEB error:', e)
        yield web.index
