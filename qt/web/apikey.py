from config import ui


def page(web):
    yield web.heading( 2, 'Edit API key')
    
    yield web.form_head('apiset')
    yield web.form_input('API key', 'key',  ui.apikey)
    yield web.form_tail()
