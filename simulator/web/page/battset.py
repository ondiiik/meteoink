from ulogging import getLogger

logger = getLogger(__name__)

from config import vbat
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    vbat["low_voltage"] = max(2.8, min(4.0, float(args["v"])))
    web.index(page)
