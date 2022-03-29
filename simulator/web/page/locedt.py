from config import location
from lang import trn
import web


@web.webpage_handler(__name__)
def www(page, args):
    loc = location[int(args['idx'])]
    page.heading(2, trn('Edit location'))
    with page.form('locset') as form:
        form.variable('idx',  args['idx'])
        form.input(trn('Location name'),    'name', loc.name)
        form.input(trn('GPS coordinates'),  'gps',  f'{loc.lat}N, {loc.lon}E')
