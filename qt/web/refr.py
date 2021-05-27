from config import ui


def page(web):
    yield web.heading( 2, 'Display refresh time')
    
    yield web.form_head('refrset')
    yield web.form_input('Refresh time', 't',  ui.refresh)
    yield web.form_input('Doubled from', 'b',  ui.dbl[0])
    yield web.form_input('Doubled to',   'e',  ui.dbl[1])
    yield web.form_tail()
