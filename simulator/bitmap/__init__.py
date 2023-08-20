from config import hw

v = hw["variant"]

if v == "acep":
    from .acep_rotated.fonts import FONTS
    from .acep_rotated.bmp import BMP
    from .acep_rotated.wind import WIND
elif v == "bwy":
    from .bwy.fonts import FONTS
    from .bwy.bmp import BMP
    from .bwy.wind import WIND
elif v == "epd47":
    from .gs.fonts import FONTS
    from .gs.bmp import BMP
    from .bwy.wind import WIND
else:
    raise TypeError(f"Don't know display type for variant {v}")
