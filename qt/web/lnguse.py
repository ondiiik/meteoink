from config import ui


def page(web):
    ui.language = web.args['l']
    ui.flush()
    return True
