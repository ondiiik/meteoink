from lang import trn
import web


@web.webpage_handler(__name__)
def www(page, args):
    page.heading(2, trn('Choose WiFi to connect'))

    with page.table(('SSID', 'BSSID', ''), 'frame="hsides"', 'style="text-align:left"') as table:
        for w in web.WebServer.net.nets:
            bssid = web.bytes2bssid(w.bssid)
            table.row((w.ssid, bssid,
                       web.button(trn('Use'), 'use', {'ssid': w.ssid, 'bssid': bssid})),
                      web.SPACES)
