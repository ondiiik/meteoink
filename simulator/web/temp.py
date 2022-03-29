from config import temp
from lang import trn
import web


@web.webpage_handler(__name__)
def www(page, args):
    page.heading(2, trn('Edit temperatures'))

    with page.form('tset') as form:
        form.input(trn('Indoor high'),  'ihi', temp.indoor_high)
        form.input(trn('Outdoor high'), 'ohi', temp.outdoor_high)
        form.input(trn('Outdoor low'),  'olo', temp.outdoor_low)
