from ulogging import getLogger

logger = getLogger(__name__)

from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("Add new location"))

    with page.form("locmake") as form:
        form.input(trn("Location name"), "name")
        form.input(trn("GPS coordinates"), "gps")
