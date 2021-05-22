from .main       import bytes2bssid, SPACES
from config      import connection, location, ui, hotspot
from config.vbat import VBAT_LOW
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
        print(location, int(i.location))
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
    
    pg += web.heading(   2,    'General setup')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('Language', ui.language, ''),                           SPACES)
    pg += web.table_row(('Units',    ui.units,    ''),                           SPACES)
    pg += web.table_row(('API key',  ui.apikey,   web.button('Edit', 'apikey')), SPACES)
    pg += web.table_tail()
    
    pg += web.heading(   2,    'Hotspot setup')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('SSID',     hotspot.ssid,   web.button('Edit', 'ssid')),   SPACES)
    pg += web.table_row(('Password', hotspot.passwd, web.button('Edit', 'passwd')), SPACES)
    pg += web.table_tail()
    
    pg += web.heading(   2,    'Battery  setup')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('Current voltage',  '{:.2f} V'.format(battery.voltage), ''),                    SPACES)
    pg += web.table_row(('Critical voltage', '{:.2f} V'.format(VBAT_LOW), web.button('Edit', 'low')), SPACES)
    pg += web.table_tail()
    
    pg += web.heading(   2,    'Misc')
    pg += web.button('Go to travel mode', 'zzz')
    
    web.write(pg)
