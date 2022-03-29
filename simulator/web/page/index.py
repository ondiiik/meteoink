from config import connection, location, ui, hotspot, alert, vbat, temp
from battery import battery
from lang import trn
import web


def index(page):
    page.heading(2, trn('Locations setup'))

    with page.table((trn('Location'), trn('Latitude'), trn('Longitude'), '', ''), 'frame="hsides"', 'style="text-align:left"') as table:
        for i in location:
            idx = {'idx': location.index(i)}
            table.row((i.name, f'{i.lat:.7f}N', f'{i.lon:.7f}E',
                       web.button(trn('Edit'),   'locedt', idx),
                       web.button(trn('Delete'), 'locdlt', idx)),
                      web.SPACES)

    page.br()
    page.button(trn('Add new location'), 'locnew')
    page.br()

    page.heading(2, trn('WiFi setup'))
    with page.table(('SSID', 'BSSID', trn('Location'), '', ''), 'frame="hsides"', 'style="text-align:left"') as table:
        for i in connection:
            if i.bssid is None:
                bssid = ''
            else:
                bssid = web.bytes2bssid(i.bssid)

            idx = {'idx': connection.index(i)}
            loc = int(i.location)
            table.row((i.ssid,
                       bssid,
                       location[loc].name if loc < len(location) else '...',
                       web.button(trn('Edit'),   'wifiedt',  idx),
                       web.button(trn('Delete'), 'wifidlt', idx)),
                      web.SPACES)

    page.br()
    page.button(trn('Add new WiFi'), 'wifinew')
    page.br()

    page.heading(2, trn('Confort temperatures'))
    with page.table(None, 'frame="hsides"') as table:
        table.row((trn('Indoor high'),  '{:.1f} °C'.format(temp.indoor_high)),  web.SPACES)
        table.row((trn('Outdoor high'), '{:.1f} °C'.format(temp.outdoor_high)), web.SPACES)
        table.row((trn('Outdoor low'),  '{:.1f} °C'.format(temp.outdoor_low)),  web.SPACES)
        table.row((web.button(trn('Edit temperatures'), 'tempedt'), ''),           web.SPACES)

    page.heading(2, trn('Alerts'))
    with page.table(None, 'frame="hsides"') as table:
        table.row((trn('Outside temperature balanced'), web.button_enable(alert.temp_balanced, 'alerttemp')), web.SPACES)
        table.row((trn('Software bug detected'),        web.button_enable(alert.error_beep,    'alertbug')), web.SPACES)

    page.heading(2, trn('General setup'))
    with page.table(None, 'frame="hsides"') as table:
        table.row((trn('Refresh time'), trn('{} min (doubled from {}:00 to {}:00)').format(ui.refresh, ui.dbl[0], ui.dbl[1]),
                   web.button(trn('Edit'), 'refredt')),   web.SPACES)
        table.row((trn('Language'),     ui.language, web.button(trn('Edit'), 'langedt')), web.SPACES)
        table.row((trn('Units'),        ui.units,    ''),                                 web.SPACES)
        table.row(('API key',           ui.apikey,   web.button(trn('Edit'), 'apiedt')),  web.SPACES)

    page.heading(2, trn('Hotspot setup'))
    with page.table(None, 'frame="hsides"') as table:
        table.row(('SSID',     hotspot.ssid,        web.button(trn('Edit'), 'ssidedt')), web.SPACES)
        table.row((trn('Password'), hotspot.passwd, web.button(trn('Edit'), 'passedt')), web.SPACES)

    page.heading(2, trn('Battery setup'))
    with page.table(None, 'frame="hsides"') as table:
        table.row((trn('Current voltage'),  '{:.2f} V'.format(battery.voltage), ''),                                  web.SPACES)
        table.row((trn('Critical voltage'), '{:.2f} V'.format(vbat.low_voltage), web.button(trn('Edit'), 'battedt')), web.SPACES)

    page.heading(2, trn('Misc'))
    page.button(trn('Go to travel mode'), 'zzz')
    page.button(trn('Go to normal mode'), 'reset')


@web.webpage_handler(__name__, 'GET')
def www(page, args):
    index(page)
