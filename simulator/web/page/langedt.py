from ulogging import getLogger
logger = getLogger(__name__)

from lang import trn
import web

_langs = 'EN', 'CZ'


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn('Choose Language'))

    with page.table((trn('Language'), ''), 'frame="hsides"', 'style="text-align:left"') as table:
        for l in _langs:
            table.row((l, web.button(trn('Use'), 'languse', {'l': l})), web.SPACES)
