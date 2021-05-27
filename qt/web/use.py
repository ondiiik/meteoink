from config import location


def page(web):
    yield web.heading( 2, 'Add new location')
    
    yield web.form_head('new')
    
    yield web.form_input('SSID',      'ssid',  web.args['ssid'])
    yield web.form_input('BSSID',     'bssid', web.args['bssid'])
    yield web.form_input('Password',  'psw')
    
    yield web.form_spacer()
    
    yield web.select_head('Location', 'location')
    
    for i in range(len(location)):
        yield web.select_option(i, location[i].name)
    
    yield web.select_tail()
    
    yield web.form_tail()
