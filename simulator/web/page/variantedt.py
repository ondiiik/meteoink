from lang import trn
from config import VARIANT_2DAYS, VARIANT_4DAYS
import web

_langs = 'EN', 'CZ'


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn('Choose forecast variant'))

    with page.table((trn('Variant'), ''), 'frame="hsides"', 'style="text-align:left"') as table:
        table.row((trn('Two days'), web.button(trn('Use'), 'variantuse', {'v': VARIANT_2DAYS})), web.SPACES)
        table.row((trn('Four days'), web.button(trn('Use'), 'variantuse', {'v': VARIANT_4DAYS})), web.SPACES)
