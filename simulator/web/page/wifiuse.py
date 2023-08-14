from db import location
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn("Add new location"))

    with page.form("wifimake") as form:
        form.input("SSID", "ssid", args["ssid"])
        form.input("BSSID", "bssid", args["bssid"])
        form.input(trn("Password"), "psw", "", "password")

        form.spacer()

        with page.select(trn("Location"), "location") as select:
            for i in range(len(location.LOCATIONS)):
                select.option(i, location.LOCATIONS[i].name)
