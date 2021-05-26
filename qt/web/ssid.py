from config import hotspot


def page(web):
    pg  = web.heading(2, 'Hotspot SSID')
    
    pg += web.form_head('ssidset')
    pg += web.form_input('SSID', 'id', hotspot.ssid)
    pg += web.form_tail()
    
    web.write(pg)
