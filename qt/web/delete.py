from micropython import const
import                  heap
from config      import connection
from .           import bytes2bssid


_spaces = const(4)


def page(web):
    pg  = web.heading( 2, 'DELETE LOCATION ??!')
    config = connection[int(web.args['idx'])]
    
    pg += web.form_head('remove')
    pg += web.form_label('SSID',     'ssid',    config.ssid)
    pg += web.form_label('BSSID',    'bssid',   bytes2bssid(config.bssid))
    pg += web.form_spacer()
    pg += web.form_label('Country',  'country', config.country)
    pg += web.form_label('City',     'city',    config.location)
    pg += web.form_tail()
    heap.refresh()
    
    web.write(pg)
