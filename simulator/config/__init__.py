print("Reading database ...")

from .base import Json
from random import choice
from os import mkdir


try:
    mkdir("cfg")
except:
    ...


alert = Json(
    "cfg/alert.json",
    {"already_triggered": False},
)

display = Json(
    "cfg/display.json",
    {"greetings": False, "lowbat": False},
)

sys = Json(
    "cfg/sys.json",
    {
        "exception_dump": 0,
        "log_level": "info",
        "led_enabled": False,
    },
)

beep = Json(
    "cfg/beep.json",
    {"temp_balanced": False, "error_beep": False},
)

location = Json(
    "cfg/location.json",
    {"locations": list()},
)

connection = Json(
    "cfg/connection.json",
    {"connections": list()},
)

spot = Json(
    "cfg/spot.json",
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
    "cfg/temp.json",
    {"indoor_high": 26, "outdoor_high": 27, "outdoor_low": -5},
)

time = Json(
    "cfg/time.json",
    {"winter": False},
)

vbat = Json(
    "cfg/vbat.json",
    {"low_voltage": 3.2, "adc2volt": 0.001757813, "show_voltage": False},
)

api = Json(
    "cfg/api.json",
    {"apikey": "", "units": "metric", "language": "en", "variant": 4},
)

behavior = Json(
    "cfg/behavior.json",
    {"refresh": 15, "dbl": (0, 7), "show_radar": 5, "display_port": 6627},
)

hw = Json(
    "cfg/hw.json",
    {
        "variant": "acep",  # Can be one of "acep" or "bwy"
        "pins": {
            "sck": 13,
            "mosi": 14,
            "miso": 12,
            "cs": 15,
            "dc": 27,
            "rst": 26,
            "busy": 25,
            "dht": 22,
            "led": 21,
            "vbat": 35,
            "buzzer": 33,
        },
        "buttons": {"hotspot": 32, "alert": -1, "sleep": -1},
    },
)
