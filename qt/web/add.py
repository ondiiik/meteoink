from web import bytes2bssid, SPACES


def page(web):
    yield web.heading( 2, 'Choose WiFi to connect')
    yield web.table_head(('SSID', 'BSSID', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for w in web.net.nets:
        bssid = bytes2bssid(w.bssid)
        yield web.table_row((w.ssid,
                             bssid,
                             web.button('Use', 'use', (('ssid', w.ssid), ('bssid', bssid)))),
                             SPACES)
    
    yield web.table_tail()
