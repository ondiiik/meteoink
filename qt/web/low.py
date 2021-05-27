from config import vbat
from lang   import trn


def page(web):
    yield web.heading( 2, trn['Critical voltage'])
    
    yield web.form_head('lowset')
    yield web.form_input(trn['Critical voltage'], 'v', vbat.low_voltage)
    yield web.form_tail()
