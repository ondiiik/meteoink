from ulogging import getLogger

logger = getLogger(__name__)

from config import api
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("Edit API key"))

    with page.form("apiset") as form:
        form.input("API key", "key", api["apikey"])
