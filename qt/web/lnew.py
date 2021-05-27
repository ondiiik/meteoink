def page(web):
    yield web.heading( 2, 'Add new location')
    yield web.form_head('nloc')
    yield web.form_input('Location name', 'name')
    yield web.form_input('Latitude',      'lat')
    yield web.form_input('Longitude',     'lon')
    yield web.form_tail()
