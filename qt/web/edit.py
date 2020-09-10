from micropython import const
from heap        import refresh
from config      import connection
from .           import bytes2bssid


_spaces = const(4)


def page(web):
    pg     = web.heading( 2, 'Edit location')
    config = connection[int(web.args['idx'])]
    
    pg += web.form_head('set')
    pg += web.form_label('SSID',     'ssid',    config.ssid)
    pg += web.form_label('BSSID',    'bssid',   bytes2bssid(config.bssid))
    pg += web.form_input('Password', 'psw',     config.passwd)
    pg += web.form_spacer()
    pg += web.form_input('Country',  'country', config.country)
    pg += web.form_input('City',     'city',    config.location)
    pg += web.form_tail()
    refresh()
    
    web.write(pg)
