import             heap
from config import connection, location
from .main  import bytes2bssid


def page(web):
    pg     = web.heading( 2, 'DELETE CONNECTION ??!')
    config = connection[int(web.args['idx'])]
    
    pg += web.form_head('rm')
    pg += web.form_label('SSID',     'ssid',    config.ssid)
    pg += web.form_label('BSSID',    'bssid',   bytes2bssid(config.bssid))
    pg += web.form_spacer()
    pg += web.form_label('Location', 'country', location[config.location].name)
    pg += web.form_tail()
    heap.refresh()
    
    web.write(pg)
