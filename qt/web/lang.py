from .main import bytes2bssid, SPACES

_langs = 'EN', 'CZ'

def page(web):
    pg  = web.heading( 2, 'Choose Language')
    pg += web.table_head(('Language', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for l in _langs:
        pg += web.table_row((l, web.button('Use', 'lnguse', (('l', l), ))), SPACES)
    
    pg += web.table_tail()
    
    web.write(pg)
