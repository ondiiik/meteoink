def page(web):
    pg  = web.heading( 2, 'Add new location')
    pg += web.form_head('nloc')
    pg += web.form_input('Location name', 'name')
    pg += web.form_input('Latitude',      'lat')
    pg += web.form_input('Longitude',     'lon')
    pg += web.form_tail()
    
    web.write(pg)
