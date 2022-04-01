from config import ui
import web


@web.action_handler(__name__)
def www(page, args):
    ui.variant = int(args['v'])
    ui.flush()

    web.index(page)
