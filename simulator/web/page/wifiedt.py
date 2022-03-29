from config import connection, location
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn('Edit connection'))
    config = connection[int(args['idx'])]

    with page.form('wifiset') as form:
        form.label('SSID',          'ssid',  config.ssid)
        form.label('BSSID',         'bssid', web.bytes2bssid(config.bssid))
        form.input(trn('Password'), 'psw',   config.passwd, 'password')
        form.spacer()

        with page.select(trn('Location'), 'location') as select:
            for i in range(len(location)):
                select.option(i, location[i].name, i == config.location)
