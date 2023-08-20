from ulogging import getLogger

logger = getLogger(__name__)

from .base import Vect, Bitmap, ZERO, ONE, TWO

from config import hw

if hw["variant"] == "acep":
    from .rotated import Canvas
else:
    from .normal import Canvas
