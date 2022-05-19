from ulogging import getLogger
logger = getLogger(__name__)

from db import location, connection
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn('DELETE CONNECTION') + ' ??!')
    config = connection.CONNECTIONS[int(args['idx'])]

    with page.form('wifirm') as form:
        form.label('SSID',     'ssid',  config.ssid)
        form.label('BSSID',    'bssid', web.bytes2bssid(config.bssid))
        form.spacer()
        form.label(trn('Location'), 'loc', location.LOCATIONS[config.location].name if config.location < len(location.LOCATIONS) else '...')
