from ulogging import getLogger

logger = getLogger(__name__)

from config import location
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("DELETE LOCATION") + " ?!")
    loc = location["locations"][int(args["idx"])]

    with page.form("locrm") as form:
        form.label(trn("Name"), "name", loc["name"])
        form.label(trn("GPS coordinates"), "gps", f"{loc['lat']}N, {loc['lon']}E")
