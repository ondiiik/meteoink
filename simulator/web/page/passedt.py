from ulogging import getLogger

logger = getLogger(__name__)

from config import spot
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("Set hotspot password"))

    with page.form("passset") as form:
        form.input(trn("Password"), "p", spot["passwd"])
