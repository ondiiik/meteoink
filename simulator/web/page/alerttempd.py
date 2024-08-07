from ulogging import getLogger

logger = getLogger(__name__)

from config import beep
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    beep["temp_balanced"] = 0
    beep.flush()
    web.index(page)
