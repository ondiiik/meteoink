from config import time
import web


@web.action_handler(__name__)
def www(page, args):
    if time.winter:
        time.winter = 0
        time.flush()

    web.index(page)
