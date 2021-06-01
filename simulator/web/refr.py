from config import ui
from lang   import trn


def page(web):
    yield web.heading( 2, trn['Display refresh time'])
    
    yield web.form_head('refrset')
    yield web.form_input(trn['Refresh time'], 't',  ui.refresh)
    yield web.form_input(trn['Doubled from'], 'b',  ui.dbl[0])
    yield web.form_input(trn['Doubled to'],   'e',  ui.dbl[1])
    yield web.form_tail()
