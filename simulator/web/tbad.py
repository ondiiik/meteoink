from config import alert
import web


@web.webpage_handler(__name__)
def www(page, args):
    if alert.temp_balanced:
        alert.temp_balanced = False
        alert.flush()

    web.index(page)
