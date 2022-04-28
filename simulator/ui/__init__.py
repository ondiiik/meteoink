from ulogging import getLogger
logger = getLogger(__name__)

from micropython import const
from .base import V, Z, Bitmap, BLACK, WHITE, GREEN, BLUE, RED, YELLOW, ORANGE, ALPHA, UiFrame, Ui

DISPLAY_REFRESH = const(0)
DISPLAY_GREETINGS = const(1)
DISPLAY_DONT_REFRESH = const(2)
