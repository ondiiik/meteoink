from ulogging import getLogger

logger = getLogger(__name__)

from db import ui
from lang import trn
import web


@web.action_handler(__name__)
def www(page, args):
    page.heading(2, trn("Display refresh time"))

    with page.form("refrset") as form:
        form.input(trn("Refresh time"), "t", ui.REFRESH)
        form.input(trn("Doubled from"), "b", ui.DBL[0])
        form.input(trn("Doubled to"), "e", ui.DBL[1])
