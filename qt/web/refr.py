from config import ui


def page(web):
    pg  = web.heading( 2, 'Display refresh time')
    
    pg += web.form_head('refrset')
    pg += web.form_input('Refresh time', 't',  ui.refresh)
    pg += web.form_input('Doubled from', 'b',  ui.dbl[0])
    pg += web.form_input('Doubled to',   'e',  ui.dbl[1])
    pg += web.form_tail()
    
    web.write(pg)
