from ulogging import getLogger

logger = getLogger(__name__)

from config import vbat
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("Critical voltage"))

    with page.form("battset") as form:
        form.input(trn("Critical voltage"), "v", vbat["low_voltage"])
