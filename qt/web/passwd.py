from config import ui


def page(web):
    yield web.heading( 2, 'Edit hotspot password:')
    
    yield web.form_head('passet')
    yield web.form_input('Password',       'p1',  '', 'password')
    yield web.form_input('Password again', 'p2',  '', 'password')
    yield web.form_tail()
