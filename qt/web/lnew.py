from lang import trn

def page(web):
    yield web.heading( 2, trn['Add new location'])
    yield web.form_head('nloc')
    yield web.form_input(trn['Location name'], 'name')
    yield web.form_input(trn['Latitude'],      'lat')
    yield web.form_input(trn['Longitude'],     'lon')
    yield web.form_tail()
