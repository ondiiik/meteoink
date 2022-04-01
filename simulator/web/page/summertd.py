from config import time
import web


@web.action_handler(__name__)
def www(page, args):
    if not time.winter:
        time.winter = 1
        time.flush()

    web.index(page)
