from ulogging import getLogger

logger = getLogger(__name__)

from config import ui
import web


@web.action_handler(__name__)
def www(page, args):
    l = int(args["t"]), (int(args["b"]), int(args["e"]))
    ui["refresh"], ui["dbl"] = l
    ui.flush()
    web.index(page)
