print("Reading database ...")

from .base import Json
from random import choice
from os import mkdir


try:
    mkdir("config")
except OSError:
    ...


alert = Json(
    "config/alert.json",
    {"already_triggered": False},
)

display = Json(
    "config/display.json",
    {"display_state": 0},
)

sys = Json(
    "config/sys.json",
    {
        "dht_humi_calib": (1, 0),
        "exception_dump": 0,
        "verbose_log": False,
        "led_enabled": False,
    },
)

beep = Json(
    "config/beep.json",
    {"temp_balanced": False, "error_beep": False},
)

location = Json(
    "config/location.json",
    {"locations": list()},
)

connection = Json(
    "config/connection.json",
    {"connections": list()},
)

spot = Json(
    "config/spot.json",
    lambda: {
        "ssid": "metoink_"
        + "".join(
            [
                choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                for _ in range(4)
            ]
        ),
        "passwd": "".join(
            [
                choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                for _ in range(12)
            ]
        ),
    },
)

temp = Json(
    "config/temp.json",
    {"indoor_high": 26, "outdoor_high": 27, "outdoor_low": -5},
)

time = Json(
    "config/time.json",
    {"winter": False},
)

vbat = Json(
    "config/vbat.json",
    {"low_voltage": 3.2, "show_voltage": False},
)

api = Json(
    "config/api.json",
    {"apikey": "", "units": "metric", "language": "en", "variant": 4},
)

ui = Json(
    "config/ui.json",
    {"refresh": 15, "dbl": (0, 7), "show_radar": 5},
)
