from web  import SPACES
from lang import trn

_langs = 'EN', 'CZ'

def page(web):
    yield web.heading( 2, trn['Choose Language'])
    yield web.table_head((trn['Language'], ''), 'frame="hsides"', 'style="text-align:left"')
    
    for l in _langs:
        yield web.table_row((l, web.button(trn['Use'], 'lnguse', (('l', l), ))), SPACES)
    
    yield web.table_tail()
