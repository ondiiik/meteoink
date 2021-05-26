from config import ui


def page(web):
    ui.apikey = web.args['key']
    ui.flush()
    return True
