from ulogging import getLogger

logger = getLogger(__name__)

from lang import trn
from net import bytes2bssid
import web


@web.action_handler(__name__)
def www(page, args):
    logger.debug(f'args: {", ".join([k+"="+v for k, v in args.items()])}')

    page.heading(2, trn("Choose WiFi to connect"))

    with page.table(
        ("SSID", "BSSID", ""), 'frame="hsides"', 'style="text-align:left"'
    ) as table:
        for w in web.WebServer.net.nets:
            bssid = bytes2bssid(w.bssid)
            table.row(
                (
                    w.ssid,
                    bssid,
                    web.button(trn("Use"), "wifiuse", {"ssid": w.ssid, "bssid": bssid}),
                ),
                web.SPACES,
            )
