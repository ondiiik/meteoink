from config import ui
import web


@web.webpage_handler(__name__)
def www(page, args):
    l = int(args['t']), (int(args['b']), int(args['e']))
    ui.refresh, ui.dbl = l
    ui.flush()

    web.index(page)
