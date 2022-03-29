from config import alert
import web


@web.webpage_handler(__name__)
def www(page, args):
    if not alert.error_beep:
        alert.error_beep = True
        alert.flush()

    web.index(page)
