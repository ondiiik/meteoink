from setup.display import MODEL
from setup import EPD_42_BWY, EPD_565_ACEP

if MODEL == EPD_565_ACEP:
    from .epd_acep import EPD
elif MODEL == EPD_42_BWY:
    from .epd_bwy import EPD
else:
    raise TypeError(f"Don't know display type {MODEL}")
