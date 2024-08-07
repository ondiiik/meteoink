from ulogging import getLogger

logger = getLogger(__name__)

from config import location
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    loc = location["locations"][int(args["idx"])]
    page.heading(2, trn("Edit location"))
    with page.form("locset") as form:
        form.variable("idx", args["idx"])
        form.input(trn("Location name"), "name", loc["name"])
        form.input(trn("GPS coordinates"), "gps", f"{loc['lat']}N, {loc['lon']}E")
