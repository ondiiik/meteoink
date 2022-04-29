from db import temp
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn('Edit temperatures'))

    with page.form('tempset') as form:
        form.input(trn('Indoor high'),  'ihi', temp.INDOOR_HIGH)
        form.input(trn('Outdoor high'), 'ohi', temp.OUTDOOR_HIGH)
        form.input(trn('Outdoor low'),  'olo', temp.OUTDOOR_LOW)
