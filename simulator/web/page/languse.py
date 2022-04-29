from db import ui
import web


@web.action_handler(__name__)
def www(page, args):
    ui.LANGUAGE = args['l']
    web.index(page)
