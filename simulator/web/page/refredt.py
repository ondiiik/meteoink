from config import ui
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn('Display refresh time'))

    with page.form('refrset') as form:
        form.input(trn('Refresh time'), 't',  ui.refresh)
        form.input(trn('Doubled from'), 'b',  ui.dbl[0])
        form.input(trn('Doubled to'),   'e',  ui.dbl[1])
