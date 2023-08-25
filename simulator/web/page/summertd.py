from ulogging import getLogger

logger = getLogger(__name__)

from config import time
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    time["winter"] = True
    time.flush()
    web.index(page)
