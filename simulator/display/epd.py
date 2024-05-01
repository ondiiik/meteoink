from config import hw

v = hw["variant"]

if v == "acep":
    from .epd_acep import EPD, ALPHA, BLACK, BLUE, GREEN, ORANGE, RED, WHITE, YELLOW
elif v == "bwy":
    from .epd_bwy import EPD, ALPHA, BLACK, WHITE, YELLOW
else:
    raise TypeError(f"Don't know display type for variant {v}")
