from config import hotspot


def page(web):
    yield web.heading(2, 'Hotspot SSID')
    
    yield web.form_head('ssidset')
    yield web.form_input('SSID', 'id', hotspot.ssid)
    yield web.form_tail()
