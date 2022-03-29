from config import hotspot
import web


@web.webpage_handler(__name__)
def www(page, args):
    p = args['p']
    hotspot.passwd = p
    hotspot.flush()

    web.index(page)
