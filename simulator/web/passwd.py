from config import hotspot
from lang   import trn


def page(web):
    yield web.heading( 2, trn['Set hotspot password'])
    
    yield web.form_head('passet')
    yield web.form_input(trn['Password'], 'p', hotspot.passwd)
    yield web.form_tail()
