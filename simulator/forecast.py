from ulogging import getLogger

logger = getLogger(__name__)

from machine import deepsleep, RTC
from micropython import const
from collections import namedtuple
from config import api, location
from ltime import Time
from buzzer import play


# See https://openweathermap.org/weather-conditions
id2icon = {
    200: "200",
    201: "200",
    202: "200",
    210: "200",
    211: "200",
    212: "200",
    221: "200",
    230: "200",
    231: "200",
    232: "200",
    300: "300",
    301: "300",
    302: "300",
    310: "300",
    311: "300",
    312: "300",
    313: "300",
    314: "300",
    321: "300",
    500: "500",
    501: "500",
    502: "500",
    503: "500",
    504: "500",
    511: "511",
    520: "520",
    521: "520",
    522: "520",
    531: "520",
    600: "600",
    601: "600",
    602: "600",
    611: "600",
    612: "600",
    613: "600",
    615: "600",
    616: "600",
    620: "600",
    621: "600",
    622: "600",
    701: "701",
    711: "701",
    721: "701",
    731: "701",
    741: "701",
    751: "701",
    761: "701",
    762: "701",
    771: "701",
    781: "701",
    800: "800",
    801: "801",
    802: "802",
    803: "803",
    804: "804",
}


DISPLAY_REFRESH_DIV = const(3)

WEATHER = const(1)
TEMPERATURE = const(2)
ALL = const(3)


class Forecast:
    Weather = namedtuple(
        "Weather",
        (
            "icon",
            "dt",
            "srt",
            "sst",
            "temp",
            "temp_mqtt",
            "feel",
            "rh",
            "rain",
            "rpb",
            "snow",
            "speed",
            "dir",
            "clouds",
        ),
    )
    Home = namedtuple("Home", ("temp", "rh"))
    Status = namedtuple("Status", ("sleep_time",))

    def __init__(self, connection, **kw):
        logger.info("Reading forecast data")
        self._read1(connection, **kw)
        self._read2(connection, api["variant"] * 24)

        self.home = Forecast.Home(kw["in_temp"], kw["in_humi"])
        self._get_status()

    @staticmethod
    def _mk_id(fid, rain):
        return fid if fid != 500 or rain < 2 else 520

    def _read1(self, connection, **kw):
        # Download weather now for today
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&mode=json&units={}&lang={}"
        current = connection.http_get_json(
            url.format(
                location["locations"][connection.config["location"]]["lat"],
                location["locations"][connection.config["location"]]["lon"],
                api["apikey"],
                api["units"],
                api["language"],
            )
        )

        # Parse todays forecast
        try:
            rain = current["rain"]["1h"]
        except KeyError:
            rain = 0.0

        rpb = current.get("pop", 0) * 100

        try:
            snow = current["snow"]["1h"]
        except KeyError:
            snow = 0.0

        self.time_zone = current["timezone"]

        weather = current["weather"][0]
        dsc = weather["description"]
        self.descr = dsc[0].upper() + dsc[1:]

        # Fix rain icon according to amount of rain
        def _mk_id(fid, rain):
            return fid if fid != 500 or rain < 0.5 else 520

        self.weather = Forecast.Weather(
            "{}{}".format(
                id2icon[self._mk_id(weather["id"], rain)], weather["icon"][-1]
            ),
            current["dt"],
            current["sys"]["sunrise"],
            current["sys"]["sunset"],
            current["main"]["temp"],
            kw.get("out_temp", None),
            current["main"]["feels_like"],
            kw.get("out_humi", None) or current["humidity"],
            rain,
            rpb,
            snow,
            current["wind"]["speed"],
            current["wind"]["deg"],
            current["clouds"],
        )
        self.time = Time(self.time_zone)

        # Set RTC clock according to forecast time
        rtc = RTC()
        dt = self.time.get_date_time(self.weather.dt)
        rtc.init((dt[0], dt[1], dt[2], 0, dt[3], dt[4], dt[5], 0))

    def _read2(self, connection, hours):
        # Download hourly weather forecast for 5 days
        url = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&mode=json&units={}&lang={}&cnt={}"
        fcast = connection.http_get_json(
            url.format(
                location["locations"][connection.config["location"]]["lat"],
                location["locations"][connection.config["location"]]["lon"],
                api["apikey"],
                api["units"],
                "EN",
                (hours + 2) // 3,
            )
        )

        # Build 2 days forecast
        self.forecast = []
        self.step = 10800
        srt = self.weather.srt
        sst = self.weather.sst

        for current in fcast["list"]:
            main = current["main"]
            weather = current["weather"][0]
            wind = current["wind"]
            clouds = current["clouds"]["all"]

            try:
                rain = current["rain"]["3h"]
            except KeyError:
                rain = 0.0

            rpb = current.get("pop", 0) * 100

            try:
                snow = current["snow"]["3h"]
            except KeyError:
                snow = 0.0

            dt = current["dt"]
            if dt > sst:
                srt += 86400
                sst += 86400

            fid = (
                701
                if current.get("visibility", 0) < 500
                and weather["id"] in range(800, 802)
                else weather["id"]
            )
            self.forecast.append(
                Forecast.Weather(
                    "{}{}".format(id2icon[self._mk_id(fid, rain)], weather["icon"][-1]),
                    dt,
                    srt,
                    sst,
                    main["temp"],
                    None,
                    main["feels_like"],
                    main["humidity"],
                    rain,
                    rpb,
                    snow,
                    wind["speed"],
                    wind["deg"],
                    clouds,
                )
            )

    def _get_status(self):
        dt = self.time.get_date_time(self.weather.dt)

        if dt[3] < 6:
            sleep_time = 30
        else:
            sleep_time = 30 // DISPLAY_REFRESH_DIV

        self.status = Forecast.Status(sleep_time)
