from ulogging import getLogger

logger = getLogger(__name__)

from db import location
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn("DELETE LOCATION") + " ?!")
    loc = location.LOCATIONS[int(args["idx"])]

    with page.form("locrm") as form:
        form.label(trn("Name"), "name", loc.name)
        form.label(trn("GPS coordinates"), "gps", f"{loc.lat}N, {loc.lon}E")
