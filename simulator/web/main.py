from ulogging import getLogger

logger = getLogger(__name__)

from . import Server
from buzzer import play
from micropython import const


SPACES = const(4)


class WebServer(Server):
    def __init__(self, net):
        super().__init__(net)
        self.last = ""

    def process(self):
        logger.info("*** PAGE ***", self.page)

        if (self.page == "") or (self.last == self.page):
            self.page = "index"

        try:
            page = __import__("web.{}".format(self.page), None, None, ("page",), 0).page
        except ImportError:
            logger.info("!!! Page {} not found !!!".format(self.page))
            return

        if not self.last == self.page:
            self.last = self.page

        play(((1047, 30), (0, 120), (1568, 30)))
        if page(self):
            page = __import__("web.index", None, None, ("page",), 0).page
            page(self)
