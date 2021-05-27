from config import temp


def page(web):
    yield web.heading( 2, 'Edit temperatures')
    
    yield web.form_head('tset')
    yield web.form_input('Indoor high',  'ihi', temp.indoor_high)
    yield web.form_input('Outdoor high', 'ohi', temp.outdoor_high)
    yield web.form_input('Outdoor low',  'olo', temp.outdoor_low)
    yield web.form_tail()
