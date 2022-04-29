from db import ui
import web


@web.action_handler(__name__)
def www(page, args):
    ui.VARIANT = int(args['v'])
    web.index(page)
