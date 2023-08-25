from ulogging import getLogger

logger = getLogger(__name__)

from config import location, connection
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("Edit connection"))
    config = connection["connections"][int(args["idx"])]

    with page.form("wifiset") as form:
        form.variable("idx", args["idx"])
        form.input("SSID", "ssid", config["ssid"])
        form.label("BSSID", "bssid", config["bssid"])
        form.checkbox(trn("Ignore BSSID"), "ib", config.get("ignore_bssid", True))
        form.input(trn("Password"), "psw", config["passwd"], "password")
        form.spacer()

        with page.select(trn("Location"), "location") as select:
            for i in range(len(location["locations"])):
                select.option(
                    i, location["locations"][i]["name"], i == config["location"]
                )
