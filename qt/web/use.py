from micropython import const
import                  heap


_spaces = const(4)


def page(web):
    pg  = web.heading( 2, 'Add new location')
    pg += web.form_head('new')
    pg += web.form_input('SSID',      'ssid',  web.args['ssid'])
    pg += web.form_input('BSSID',     'bssid', web.args['bssid'])
    pg += web.form_input('Password',  'psw')
    pg += web.form_spacer()
    pg += web.form_input('Location',  'location')
    pg += web.form_input('Latitude',  'lat')
    pg += web.form_input('Longitude', 'lon')
    pg += web.form_tail()
    heap.refresh()
    
    web.write(pg)
