from db import ui
import web


@web.action_handler(__name__)
def www(page, args):
    ui.APIKEY = args['key']
    web.index(page)
