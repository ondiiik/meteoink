from config import ui


def page(web):
    ui.refresh = web.args['t']
    ui.flush()
    return True
