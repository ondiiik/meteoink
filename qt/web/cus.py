from config import connection, location
from log import dump_exception
from lang import trn


def page(web):
    try:
        yield web.heading( 2, trn['Add new WiFi'])

        yield web.form_head('new')

        yield web.form_input('SSID', 'ssid')
        yield web.form_input(trn['Password'], 'psw', '', 'password')

        yield web.form_spacer()

        yield web.select_head(trn['Location'], 'location')

        for i in range(len(location)):
            yield web.select_option(i, location[i].name)

        yield web.select_tail()

        yield web.form_tail()

    except Exception as e:
        dump_exception('WEB error:', e)
        yield web.index
