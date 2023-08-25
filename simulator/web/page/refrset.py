from ulogging import getLogger

logger = getLogger(__name__)

from config import behavior
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    l = int(args["t"]), (int(args["b"]), int(args["e"]))
    behavior["refresh"], behavior["dbl"] = l
    behavior.flush()
    web.index(page)
