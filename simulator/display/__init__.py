from ulogging import getLogger
logger = getLogger(__name__)

from .base import BLACK, WHITE, GREEN, BLUE, RED, YELLOW, ORANGE, ALPHA
from .base import Vect, Bitmap, Frame

from setup.display import DISPLAY_ROTATED

if DISPLAY_ROTATED:
    from .rotated import Canvas
else:
    from .normal import Canvas
