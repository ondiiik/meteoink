from ulogging import getLogger

logger = getLogger(__name__)

from config import spot
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn("Hotspot SSID"))

    with page.form("ssidset") as form:
        form.input("SSID", "id", spot["ssid"])
