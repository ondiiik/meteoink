from db import beep
import web


@web.action_handler(__name__)
def www(page, args):
    beep.ERROR_BEEP = 0
    web.index(page)
