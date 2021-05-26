from config import ui


def page(web):
    pg  = web.heading( 2, 'Edit hotspot password:')
    
    pg += web.form_head('passet')
    pg += web.form_input('Password',       'p1',  '', 'password')
    pg += web.form_input('Password again', 'p2',  '', 'password')
    pg += web.form_tail()
    
    web.write(pg)
