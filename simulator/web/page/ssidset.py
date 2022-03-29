from config import hotspot
import web


@web.action_handler(__name__)
def www(page, args):
    hotspot.ssid = args['id']
    hotspot.flush()

    web.index(page)
