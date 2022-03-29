from config import connection, location
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn('DELETE CONNECTION') + ' ??!')
    config = connection[int(args['idx'])]

    with page.form('wifirm') as form:
        form.label('SSID',     'ssid',  config.ssid)
        form.label('BSSID',    'bssid', web.bytes2bssid(config.bssid))
        form.spacer()
        form.label(trn('Location'), 'loc', location[config.location].name if config.location < len(location) else '...')
