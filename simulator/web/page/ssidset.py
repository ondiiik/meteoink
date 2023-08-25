from ulogging import getLogger

logger = getLogger(__name__)

from config import spot
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    spot["ssid"] = args["id"]
    spot.flush()
    web.index(page)
