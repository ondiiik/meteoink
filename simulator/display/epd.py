# Display selection
#
# Display drivers are provided by `ueink` library (see `libs/ueink`). This module
# selects driver for configured HW variant and exports its colors as constants
# (`BLACK`, `WHITE`, `YELLOW`, ...). Only colors supported by selected display
# are exported, so UI can detect missing colors by `ImportError`.
#
# Adding of new display variant then means just to add new branch bellow.
from micropython import const
from config import hw

from .panel import Panel


VARIANT = hw["variant"]

if VARIANT == "acep":
    # WaveShare 5.65inch e-Paper Module (F), 600 x 448, 7 colors
    from ueink.epd_ws565_acep import Epd

    _ROTATED = True
    _DEGHOST = True
elif VARIANT == "bwy":
    # WaveShare 4.2inch e-Paper Module (C) - black/white/yellow, 400 x 300
    from ueink.epd_ws420_3c_yellow import Epd

    _ROTATED = False
    _DEGHOST = False
else:
    raise TypeError(f"Don't know display type for variant {VARIANT}")


# Transparent color used as key for bitmaps blitting (never flushed to display)
ALPHA = const(7)

for _name, _index in Epd.color.items():
    globals()[_name.upper()] = _index


class EPD(Panel):
    DRIVER = Epd
    ROTATED = _ROTATED
    DEGHOST = _DEGHOST
