from config import vbat
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn('Critical voltage'))

    with page.form('battset') as form:
        form.input(trn('Critical voltage'), 'v', vbat.low_voltage)
