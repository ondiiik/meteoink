from ulogging import getLogger

logger = getLogger(__name__)

from config import api
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    api["variant"] = int(args["v"])
    web.index(page)
