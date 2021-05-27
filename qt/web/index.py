from web         import bytes2bssid, SPACES
from config      import connection, location, ui, hotspot, alert, vbat, temp
from battery     import battery
from lang        import trn


def page(web):
    yield web.heading( 2,trn['Locations setup'])
    
    yield web.table_head((trn['Location'], trn['Latitude'], trn['Longitude'], '', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for i in location:
        idx = (('idx', location.index(i)),)
        yield web.table_row((i.name, i.lat, i.lon,
                             web.button(trn['Edit'],   'led',  idx),
                             web.button(trn['Delete'], 'ldlt', idx)),
                             SPACES)
    
    yield web.table_tail()
    yield web.br()
    yield web.button(trn['Add new location'], 'lnew')
    yield web.br()
    
    yield web.heading(2, trn['WiFi setup'])
    yield web.table_head(('SSID', 'BSSID', trn['Location'],'', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for i in connection:
        if i.bssid is None:
            bssid = ''
        else:
            bssid = bytes2bssid(i.bssid)
        
        idx = (('idx', connection.index(i)),)
        loc = int(i.location)
        yield web.table_row((i.ssid,
                             bssid,
                             location[loc].name if loc < len(location) else '...',
                             web.button(trn['Edit'],   'ed',  idx),
                             web.button(trn['Delete'], 'dlt', idx)),
                             SPACES)
    
    yield web.table_tail()
    yield web.br()
    yield web.button(trn['Add new WiFi'], 'add')
    yield web.br()
    
    yield web.heading(2, trn['Confort temperatures'])
    yield web.table_head(None, 'frame="hsides"')
    yield web.table_row((trn['Indoor high'],  '{:.1f} °C'.format(temp.indoor_high)),  SPACES)
    yield web.table_row((trn['Outdoor high'], '{:.1f} °C'.format(temp.outdoor_high)), SPACES)
    yield web.table_row((trn['Outdoor low'],  '{:.1f} °C'.format(temp.outdoor_low)),  SPACES)
    yield web.table_row((web.button(trn['Edit temperatures'], 'temp'),''),            SPACES)
    yield web.table_tail()
    
    yield web.heading(2, trn['Alerts'])
    yield web.table_head(None, 'frame="hsides"')
    yield web.table_row((trn['Outside temperature balanced'], web.button_enable(alert.temp_balanced, 'tba')), SPACES)
    yield web.table_row((trn['Software bug detected'],        web.button_enable(alert.error_beep,    'swb')), SPACES)
    yield web.table_tail()
    
    yield web.heading(2, trn['General setup'])
    yield web.table_head(None, 'frame="hsides"')
    yield web.table_row((trn['Refresh time'], trn['{} min (doubled from {}:00 to {}:00)'].format(ui.refresh, ui.dbl[0], ui.dbl[1]),
                                                           web.button(trn['Edit'], 'refr')),   SPACES)
    yield web.table_row((trn['Language'],     ui.language, web.button(trn['Edit'], 'lang')),   SPACES)
    yield web.table_row((trn['Units'],        ui.units,    ''),                                SPACES)
    yield web.table_row(('API key',      ui.apikey,   web.button(trn['Edit'],      'apikey')), SPACES)
    yield web.table_tail()
    
    yield web.heading(2, trn['Hotspot setup'])
    yield web.table_head(None, 'frame="hsides"')
    yield web.table_row(('SSID',     hotspot.ssid,   web.button(trn['Edit'], 'ssid')),   SPACES)
    yield web.table_row((trn['Password'], hotspot.passwd, web.button(trn['Edit'], 'passwd')), SPACES)
    yield web.table_tail()
    
    yield web.heading(2, trn['Battery setup'])
    yield web.table_head(None, 'frame="hsides"')
    yield web.table_row((trn['Current voltage'],  '{:.2f} V'.format(battery.voltage), ''),                              SPACES)
    yield web.table_row((trn['Critical voltage'], '{:.2f} V'.format(vbat.low_voltage), web.button(trn['Edit'], 'low')), SPACES)
    yield web.table_tail()
    
    yield web.heading(2, trn['Misc'])
    yield web.button(trn['Go to travel mode'], 'zzz')
    yield web.button(trn['Go to normal mode'], 'res')
