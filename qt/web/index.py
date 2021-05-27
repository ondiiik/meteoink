from .main       import bytes2bssid, SPACES
from config      import connection, location, ui, hotspot, alert, vbat, temp
from battery     import battery
from lang        import trn


def page(web):
    pg  = web.heading( 2,trn['Locations setup'])
    
    pg += web.table_head((trn['Location'], 'Latitude', 'Longitude', '', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for i in location:
        idx = (('idx', location.index(i)),)
        pg += web.table_row((i.name, i.lat, i.lon,
                             web.button(trn['Edit'],   'led',  idx),
                             web.button(trn['Delete'], 'ldlt', idx)),
                             SPACES)
    
    pg += web.table_tail()
    pg += web.br()
    pg += web.button(trn['Add new location'], 'lnew')
    pg += web.br()
    
    pg += web.heading(2, trn['WiFi setup'])
    pg += web.table_head(('SSID', 'BSSID', 'Location','', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for i in connection:
        if i.bssid is None:
            bssid = ''
        else:
            bssid = bytes2bssid(i.bssid)
        
        idx = (('idx', connection.index(i)),)
        pg += web.table_row((i.ssid,
                             bssid,
                             location[int(i.location)].name,
                             web.button(trn['Edit'],   'ed',  idx),
                             web.button(trn['Delete'], 'dlt', idx)),
                             SPACES)
    
    pg += web.table_tail()
    pg += web.br()
    pg += web.button(trn['Add new WiFi'], 'add')
    pg += web.br()
    
    pg += web.heading(2, trn['Confort temperatures'])
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row((trn['Indoor high'],  '{:.1f} °C'.format(temp.indoor_high)),  SPACES)
    pg += web.table_row((trn['Outdoor high'], '{:.1f} °C'.format(temp.outdoor_high)), SPACES)
    pg += web.table_row((trn['Outdoor low'],  '{:.1f} °C'.format(temp.outdoor_low)),  SPACES)
    pg += web.table_row((web.button(trn['Edit temperatures'], 'temp'),''),            SPACES)
    pg += web.table_tail()
    
    pg += web.heading(2, trn['Alerts'])
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row((trn['Outside temperature balanced'], web.button_enable(alert.temp_balanced, 'tba')), SPACES)
    pg += web.table_row((trn['Software bug detected'],        web.button_enable(alert.error_beep,    'swb')), SPACES)
    pg += web.table_tail()
    
    pg += web.heading(2, trn['General setup'])
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row((trn['Refresh time'], trn['{} min (doubled from {}:00 to {}:00)'].format(ui.refresh, ui.dbl[0], ui.dbl[1]),
                                                           web.button(trn['Edit'], 'refr')), SPACES)
    pg += web.table_row((trn['Language'],     ui.language, web.button(trn['Edit'], 'lang')), SPACES)
    pg += web.table_row((trn['Units'],        ui.units,    ''),                              SPACES)
    pg += web.table_row(('API key',      ui.apikey,   web.button(trn['Edit'], 'apikey')),    SPACES)
    pg += web.table_tail()
    
    pg += web.heading(2, trn['Hotspot setup'])
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('SSID',     hotspot.ssid,   web.button(trn['Edit'], 'ssid')),   SPACES)
    pg += web.table_row(('Password', hotspot.passwd, web.button(trn['Edit'], 'passwd')), SPACES)
    pg += web.table_tail()
    
    pg += web.heading(2, 'Battery  setup')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('Current voltage',  '{:.2f} V'.format(battery.voltage), ''),                              SPACES)
    pg += web.table_row(('Critical voltage', '{:.2f} V'.format(vbat.low_voltage), web.button(trn['Edit'], 'low')), SPACES)
    pg += web.table_tail()
    
    pg += web.heading(2, trn['Misc'])
    pg += web.button(trn['Go to travel mode'], 'zzz')
    pg += web.button(trn['Go to normal mode'], 'reset')
    
    web.write(pg)
