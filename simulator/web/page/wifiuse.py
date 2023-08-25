from ulogging import getLogger

logger = getLogger(__name__)

from config import location
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("Add new location"))

    with page.form("wifimake") as form:
        form.input("SSID", "ssid", args["ssid"])
        form.input("BSSID", "bssid", args["bssid"])
        form.input(trn("Password"), "psw", "", "password")
        form.checkbox(trn("Ignore BSSID"), "ib")

        form.spacer()

        with page.select(trn("Location"), "location") as select:
            for i, l in enumerate(location["locations"]):
                select.option(i, l["name"])
