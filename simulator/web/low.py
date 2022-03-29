from config import vbat
from lang import trn
import web


@web.webpage_handler(__name__)
def www(page, args):
    page.heading(2, trn('Critical voltage'))

    with page.form('lowset') as form:
        form.input(trn('Critical voltage'), 'v', vbat.low_voltage)
