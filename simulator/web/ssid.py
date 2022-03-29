from config import hotspot
from lang import trn
import web


@web.webpage_handler(__name__)
def www(page, args):
    page.heading(2, trn('Hotspot SSID'))

    with page.form('ssidset') as form:
        form.input('SSID', 'id', hotspot.ssid)
