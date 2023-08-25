from ulogging import getLogger

logger = getLogger(__name__)

from config import temp
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("Edit temperatures"))

    with page.form("tempset") as form:
        form.input(trn("Indoor high"), "ihi", temp["indoor_high"])
        form.input(trn("Outdoor high"), "ohi", temp["outdoor_high"])
        form.input(trn("Outdoor low"), "olo", temp["outdoor_low"])
