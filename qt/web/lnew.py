from micropython import const
import                  heap


_spaces = const(4)


def page(web):
    pg  = web.heading( 2, 'Add new location')
    pg += web.form_head('nloc')
    pg += web.form_input('Location name', 'name')
    pg += web.form_input('Latitude',      'lat')
    pg += web.form_input('Longitude',     'lon')
    pg += web.form_tail()
    heap.refresh()
    
    web.write(pg)
