from .main import bytes2bssid, SPACES


def page(web):
    pg  = web.heading( 2, 'Choose WiFi to connect')
    pg += web.table_head(('SSID', 'BSSID', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for w in web.net.nets:
        bssid = bytes2bssid(w.bssid)
        pg   += web.table_row((w.ssid,
                               bssid,
                               web.button('Use', 'use', (('ssid', w.ssid), ('bssid', bssid)))),
                               SPACES)
    
    pg += web.table_tail()
    
    web.write(pg)
