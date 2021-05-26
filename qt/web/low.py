from config import vbat


def page(web):
    pg  = web.heading( 2, 'Low voltage limit')
    
    pg += web.form_head('lowset')
    pg += web.form_input('Low battery voltage', 'v', vbat.low_voltage)
    pg += web.form_tail()
    
    web.write(pg)
