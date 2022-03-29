from lang import trn
import web

_langs = 'EN', 'CZ'


@web.webpage_handler(__name__)
def www(page, args):
    page.heading(2, trn('Choose Language'))

    with page.table((trn('Language'), ''), 'frame="hsides"', 'style="text-align:left"') as table:
        for l in _langs:
            table.row((l, web.button(trn('Use'), 'lnguse', {'l': l})), web.SPACES)
