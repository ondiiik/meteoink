from micropython import const
import                  heap
from config      import location


_spaces = const(4)


def page(web):
    pg  = web.heading( 2, 'Add new location')
    
    pg += web.form_head('new')
    
    pg += web.form_input('SSID',      'ssid',  web.args['ssid'])
    pg += web.form_input('BSSID',     'bssid', web.args['bssid'])
    pg += web.form_input('Password',  'psw')
    
    pg += web.form_spacer()
    
    pg += web.select_head('Location', 'location')
    
    for i in range(len(location)):
        pg += web.select_option(i, location[i].name)
    
    pg += web.select_tail()
    
    pg += web.form_tail()
    heap.refresh()
    
    web.write(pg)
