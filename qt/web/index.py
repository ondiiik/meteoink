from .main       import bytes2bssid, SPACES
from config      import connection, location, ui, hotspot, alert, vbat, temp
from battery     import battery


def page(web):
    pg  = web.heading( 2,'Locations setup')
    
    pg += web.table_head(('Location', 'Latitude', 'Longitude', '', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for i in location:
        idx = (('idx', location.index(i)),)
        pg += web.table_row((i.name, i.lat, i.lon,
                             web.button('Edit',   'led',  idx),
                             web.button('Delete', 'ldlt', idx)),
                             SPACES)
    
    pg += web.table_tail()
    pg += web.br()
    pg += web.button('Add new location', 'lnew')
    pg += web.br()
    
    pg += web.heading( 2,'WiFi setup')
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
                             web.button('Edit',   'ed',  idx),
                             web.button('Delete', 'dlt', idx)),
                             SPACES)
    
    pg += web.table_tail()
    pg += web.br()
    pg += web.button('Add new WiFi', 'add')
    pg += web.br()
    
    pg += web.heading(   2,    'Confort temperatures')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('Indoor high',  '{:.1f} V'.format(temp.indoor_high)),  SPACES)
    pg += web.table_row(('Outdoor high', '{:.1f} V'.format(temp.outdoor_high)), SPACES)
    pg += web.table_row(('Outdoor low',  '{:.1f} V'.format(temp.outdoor_low)),  SPACES)
    pg += web.table_row((web.button('Edit temperatures', 'temp'),''),           SPACES)
    pg += web.table_tail()
    
    pg += web.heading(   2,    'Alerts')
    pg += web.table_head(None, 'frame="hsides"')
    
    name = 'Disable' if alert.temp_balanced else 'Enable'
    page = 'tbad'    if alert.temp_balanced else 'tbae'
    
    pg += web.table_row(('Outside temperature balanced', web.button(name, page)), SPACES)
    pg += web.table_tail()
    
    pg += web.heading(   2,    'General setup')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('Refresh time', ui.refresh,  web.button('Edit', 'refr')),   SPACES)
    pg += web.table_row(('Language',     ui.language, web.button('Edit', 'lang')),   SPACES)
    pg += web.table_row(('Units',        ui.units,    ''),                           SPACES)
    pg += web.table_row(('API key',      ui.apikey,   web.button('Edit', 'apikey')), SPACES)
    pg += web.table_tail()
    
    pg += web.heading(   2,    'Hotspot setup')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('SSID',     hotspot.ssid,   web.button('Edit', 'ssid')),   SPACES)
    pg += web.table_row(('Password', hotspot.passwd, web.button('Edit', 'passwd')), SPACES)
    pg += web.table_tail()
    
    pg += web.heading(   2,    'Battery  setup')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('Current voltage',  '{:.2f} V'.format(battery.voltage), ''),                         SPACES)
    pg += web.table_row(('Critical voltage', '{:.2f} V'.format(vbat.low_voltage), web.button('Edit', 'low')), SPACES)
    pg += web.table_tail()
    
    pg += web.heading(   2,    'Misc')
    pg += web.button('Go to travel mode', 'zzz')
    pg += web.button('Go to normal mode', 'reset')
    
    web.write(pg)
