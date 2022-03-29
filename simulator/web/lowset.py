from config import vbat
import web


@web.webpage_handler(__name__)
def www(page, args):
    vbat.low_voltage = max(2.8, min(4.0, float(args['v'])))
    vbat.flush()

    web.index(page)
