from db import ui
import web


@web.action_handler(__name__)
def www(page, args):
    l = int(args['t']), (int(args['b']), int(args['e']))
    ui.REFRESH, ui.DBL = l
    web.index(page)
