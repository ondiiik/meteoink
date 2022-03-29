from config import ui
import web


@web.webpage_handler(__name__)
def www(page, args):
    ui.language = args['l']
    ui.flush()

    web.index(page)
