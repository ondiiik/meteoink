from ulogging import getLogger
logger = getLogger(__name__)

from lang import trn
import web

_langs = 'EN', 'CZ'


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn('Choose forecast variant'))

    with page.table((trn('Variant'), ''), 'frame="hsides"', 'style="text-align:left"') as table:
        table.row((trn('Two days'), web.button(trn('Use'), 'variantuse', {'v': 2})), web.SPACES)
        table.row((trn('Four days'), web.button(trn('Use'), 'variantuse', {'v': 4})), web.SPACES)
