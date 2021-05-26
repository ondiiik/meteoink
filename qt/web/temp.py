from config import temp


def page(web):
    pg  = web.heading( 2, 'Edit temperatures')
    
    pg += web.form_head('tset')
    pg += web.form_input('Indoor high',  'ihi', temp.indoor_high)
    pg += web.form_input('Outdoor high', 'ohi', temp.outdoor_high)
    pg += web.form_input('Outdoor low',  'olo', temp.outdoor_low)
    pg += web.form_tail()
    
    web.write(pg)
