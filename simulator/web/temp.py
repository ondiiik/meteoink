from config import temp
from lang   import trn


def page(web):
    yield web.heading(2, trn['Edit temperatures'])
    
    yield web.form_head('tset')
    yield web.form_input(trn['Indoor high'],  'ihi', temp.indoor_high)
    yield web.form_input(trn['Outdoor high'], 'ohi', temp.outdoor_high)
    yield web.form_input(trn['Outdoor low'],  'olo', temp.outdoor_low)
    yield web.form_tail()
