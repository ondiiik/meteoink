from config import hw

v = hw["variant"]

if v == "acep":
    from .acep.main import MeteoUi
elif v == "bwy":
    from .bwy.main import MeteoUi
else:
    raise TypeError(f"Don't know display type for variant {v}")
