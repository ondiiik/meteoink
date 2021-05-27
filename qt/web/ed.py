from config import connection, location
from log    import dump_exception
from web    import bytes2bssid
from lang   import trn


def page(web):
    try:
        yield web.heading( 2, trn['Edit connection'])
        config = connection[int(web.args['idx'])]
        
        yield web.form_head('set')
        
        yield web.form_label('SSID',          'ssid',  config.ssid)
        yield web.form_label('BSSID',         'bssid', bytes2bssid(config.bssid))
        yield web.form_input(trn['Password'], 'psw',   config.passwd, 'password')
        
        yield web.form_spacer()
        
        yield web.select_head(trn['Location'], 'location')
        
        for i in range(len(location)):
            yield web.select_option(i, location[i].name, i == config.location)
            
        yield web.select_tail()
        
        yield web.form_tail()
        
    except Exception as e:
        dump_exception('WEB error:', e)
        yield web.index
