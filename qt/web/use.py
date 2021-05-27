from config import location
from lang   import trn


def page(web):
    yield web.heading(2, trn['Add new location'])
    
    yield web.form_head('new')
    
    yield web.form_input('SSID',          'ssid',  web.args['ssid'])
    yield web.form_input('BSSID',         'bssid', web.args['bssid'])
    yield web.form_input(trn['Password'], 'psw')
    
    yield web.form_spacer()
    
    yield web.select_head(trn['Location'], 'location')
    
    for i in range(len(location)):
        yield web.select_option(i, location[i].name)
    
    yield web.select_tail()
    
    yield web.form_tail()
