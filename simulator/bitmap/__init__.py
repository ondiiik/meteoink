from setup.display import MODEL
from setup import EPD_42_BWY, EPD_565_ACEP

if MODEL == EPD_565_ACEP:
    from .acep_rotated import bmp, fonts
elif MODEL == EPD_42_BWY:
    from .bwy import bmp, fonts
else:
    raise TypeError(f"Don't know display type {MODEL}")
