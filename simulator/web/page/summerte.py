from db import time
import web


@web.action_handler(__name__)
def www(page, args):
    time.WINTER = False
    web.index(page)
