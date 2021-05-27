from config import connection, location
from .main  import bytes2bssid
from log    import dump_exception


def page(web):
    try:
        pg     = web.heading( 2, 'Edit connection')
        config = connection[int(web.args['idx'])]
        
        pg += web.form_head('set')
        
        pg += web.form_label('SSID',     'ssid',      config.ssid)
        pg += web.form_label('BSSID',    'bssid',     bytes2bssid(config.bssid))
        pg += web.form_input('Password', 'psw',       config.passwd, 'password')
        
        pg += web.form_spacer()
        
        pg += web.select_head('Location', 'location')
        
        for i in range(len(location)):
            pg += web.select_option(i, location[i].name, i == config.location)
            
        pg += web.select_tail()
        
        pg += web.form_tail()
        
        web.write(pg)
        
    except Exception as e:
        dump_exception('WEB error:', e)
        return True
