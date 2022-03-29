from config import alert
import web


@web.action_handler(__name__)
def www(page, args):
    if alert.error_beep:
        alert.error_beep = False
        alert.flush()

    web.index(page)
