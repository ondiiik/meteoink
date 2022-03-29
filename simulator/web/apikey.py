from config import ui
from lang import trn
import web


@web.webpage_handler(__name__)
def www(page, args):
    page.heading(2, trn('Edit API key'))

    with page.form('apiset') as form:
        form.input('API key', 'key',  ui.apikey)
