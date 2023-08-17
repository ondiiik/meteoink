print("Reading database ...")

from .base import Json
from random import choice
from os import mkdir


alert = Json(
    "alert.json",
    {"already_triggered": False},
)

display = Json(
    "display.json",
    {"display_state": 0},
)

sys = Json(
    "sys.json",
    {
        "dht_humi_calib": (1, 0),
        "exception_dump": 0,
        "verbose_log": False,
        "led_enabled": False,
    },
)

beep = Json(
    "beep.json",
    {"temp_balanced": False, "error_beep": False},
)

location = Json(
    "location.json",
    {"locations": list()},
)

connection = Json(
    "connection.json",
    {"connections": list()},
)

spot = Json(
    "spot.json",
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
    "temp.json",
    {"indoor_high": 26, "outdoor_high": 27, "outdoor_low": -5},
)

time = Json(
    "time.json",
    {"winter": False},
)

vbat = Json(
    "vbat.json",
    {"low_voltage": 3.2, "show_voltage": False},
)

api = Json(
    "api.json",
    {"apikey": "", "units": "metric", "language": "en", "variant": 4},
)

ui = Json(
    "ui.json",
    {"refresh": 15, "dbl": (0, 7), "show_radar": 5},
)
