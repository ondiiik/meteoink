from web import bytes2bssid, SPACES

_langs = 'EN', 'CZ'

def page(web):
    yield web.heading( 2, 'Choose Language')
    yield web.table_head(('Language', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for l in _langs:
        yield web.table_row((l, web.button('Use', 'lnguse', (('l', l), ))), SPACES)
    
    yield web.table_tail()
