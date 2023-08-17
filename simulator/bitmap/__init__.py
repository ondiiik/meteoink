from setup.display import MODEL
from variant import EPD_42_BWY, EPD_565_ACEP

if MODEL == EPD_565_ACEP:
    from .acep_rotated.fonts import FONTS
    from .acep_rotated.bmp import BMP
    from .acep_rotated.wind import WIND
elif MODEL == EPD_42_BWY:
    from .bwy.fonts import FONTS
    from .bwy.bmp import BMP
    from .bwy.wind import WIND
else:
    raise TypeError(f"Don't know display type {MODEL}")
