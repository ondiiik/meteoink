from config import vbat


def page(web):
    yield web.heading( 2, 'Low voltage limit')
    
    yield web.form_head('lowset')
    yield web.form_input('Low battery voltage', 'v', vbat.low_voltage)
    yield web.form_tail()
