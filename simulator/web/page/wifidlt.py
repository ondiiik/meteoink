from ulogging import getLogger

logger = getLogger(__name__)

from config import location, connection
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("DELETE CONNECTION") + " ?!")
    config = connection["connections"][int(args["idx"])]

    with page.form("wifirm") as form:
        form.label("SSID", "ssid", config["ssid"])
        form.label("BSSID", "bssid", config["bssid"])
        form.spacer()
        form.label(
            trn("Location"),
            "loc",
            location["locations"][config["location"]]["name"]
            if config["location"] < len(location["locations"])
            else "...",
        )
