from config import location
from lang import trn
import web


@web.webpage_handler(__name__)
def www(page, args):
    page.heading(2, trn('Add new location'))

    with page.form('new') as form:
        form.input('SSID',          'ssid',  args['ssid'])
        form.input('BSSID',         'bssid', args['bssid'])
        form.input(trn('Password'), 'psw',   config.passwd, 'password')

        form.spacer()

        with page.select(trn('Location'), 'location') as select:
            for i in range(len(location)):
                select.option(i, location[i].name)
