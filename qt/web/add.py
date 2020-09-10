from micropython import const
from heap        import refresh
from .           import bytes2bssid


_spaces = const(4)


def page(web):
    pg  = web.heading( 2, 'Choose WiFi to connect')
    pg += web.table_head(('SSID', 'BSSID', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for w in web.net.nets:
        refresh()
        bssid = bytes2bssid(w.bssid)
        pg   += web.table_row((w.ssid,
                               bssid,
                               web.button('Use', 'use', (('ssid', w.ssid), ('bssid', bssid)))),
                               _spaces)
    
    pg += web.table_tail()
    refresh()
    
    web.write(pg)
