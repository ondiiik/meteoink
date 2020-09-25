from micropython import const
import                  heap
from config      import connection
from .           import bytes2bssid


_spaces = const(4)


def page(web):
    pg     = web.heading( 2, 'Edit location')
    config = connection[int(web.args['idx'])]
    
    pg += web.form_head('set')
    pg += web.form_label('SSID',     'ssid',      config.ssid)
    pg += web.form_label('BSSID',    'bssid',     bytes2bssid(config.bssid))
    pg += web.form_input('Password', 'psw',       config.passwd)
    pg += web.form_spacer()
    pg += web.form_input('Location',  'location', config.location)
    pg += web.form_input('Latitude',  'lat',      config.lat)
    pg += web.form_input('Longitude', 'lon',      config.lon)
    pg += web.form_tail()
    heap.refresh()
    
    web.write(pg)
