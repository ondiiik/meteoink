from config import ui


def page(web):
    pg  = web.heading( 2, 'Display refresh time')
    
    pg += web.form_head('refrset')
    pg += web.form_input('Refresh time', 't',  ui.refresh)
    pg += web.form_tail()
    
    web.write(pg)
