from ulogging import getLogger

logger = getLogger(__name__)

from config import behavior
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("Display refresh time"))

    with page.form("refrset") as form:
        form.input(trn("Refresh time"), "t", behavior["refresh"])
        form.input(trn("Doubled from"), "b", behavior["dbl"][0])
        form.input(trn("Doubled to"), "e", behavior["dbl"][1])
