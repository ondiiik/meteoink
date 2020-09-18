from micropython import const
import                  heap
from .           import bytes2bssid


_spaces = const(4)


def page(web):
    from config import connection, ui, hotspot, vbat
    from vbat   import voltage
    
    pg  = web.heading( 2, 'Locations setup')
    pg += web.table_head(('SSID', 'BSSID', 'Country', 'Location', '', ''), 'frame="hsides"', 'style="text-align:left"')
    
    for place in connection:
        heap.refresh()
        
        if place.bssid is None:
            bssid = ''
        else:
            bssid = bytes2bssid(place.bssid)
        
        idx = (('idx', connection.index(place)),)
        pg += web.table_row((place.ssid,
                             bssid,
                             place.country,
                             place.location,
                             web.button('Edit',   'edit',   idx),
                             web.button('Delete', 'delete', idx)),
                             _spaces)
    
    pg += web.table_tail()
    heap.refresh()
    
    pg += web.br()
    pg += web.button('Add new location', 'add')
    pg += web.br()
    heap.refresh()
    
    pg += web.heading(   2,    'General setup')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('Language', ui.language, ''),                           _spaces)
    pg += web.table_row(('Units',    ui.units,    ''),                           _spaces)
    pg += web.table_row(('API key',  ui.apikey,   web.button('Edit', 'apikey')), _spaces)
    pg += web.table_tail()
    
    pg += web.heading(   2,    'Hotspot setup')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('SSID',     hotspot.ssid,   web.button('Edit', 'ssid')),   _spaces)
    pg += web.table_row(('Password', hotspot.passwd, web.button('Edit', 'passwd')), _spaces)
    pg += web.table_tail()
    
    pg += web.heading(   2,    'Battery  setup')
    pg += web.table_head(None, 'frame="hsides"')
    pg += web.table_row(('Current voltage',  '{:.2f} V'.format(voltage()), ''),                                 _spaces)
    pg += web.table_row(('Critical voltage', '{:.2f} V'.format(vbat.VBAT_LOW), web.button('Edit', 'low')), _spaces)
    pg += web.table_tail()
    
    web.write(pg)
