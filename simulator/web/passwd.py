from config import hotspot
from lang import trn
import web


@web.webpage_handler(__name__)
def www(page, args):
    page.heading(2, trn('Set hotspot password'))

    with page.form('passet') as form:
        form.input(trn('Password'), 'p', hotspot.passwd)
