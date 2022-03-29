from config import ui
import web


@web.action_handler(__name__)
def www(page, args):
    ui.apikey = args['key']
    ui.flush()

    web.index(page)
