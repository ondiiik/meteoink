from config import ui


def page(web):
    pg  = web.heading( 2, 'Edit API key')
    
    pg += web.form_head('apiset')
    pg += web.form_input('API key', 'key',  ui.apikey)
    pg += web.form_tail()
    
    web.write(pg)
