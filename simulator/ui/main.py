from ulogging import getLogger

logger = getLogger(__name__)

from setup.display import MODEL
from setup import EPD_42_BWY, EPD_565_ACEP

if MODEL == EPD_565_ACEP:
    from .acep.main import Epd
elif MODEL == EPD_42_BWY:
    from .bwy.main import Epd
else:
    raise TypeError(f"Don't know display type {MODEL}")


class MeteoUi(Epd):
    pass
