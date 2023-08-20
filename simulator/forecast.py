from ulogging import getLogger

logger = getLogger(__name__)

import dht
from machine import Pin, deepsleep, RTC
from micropython import const
from collections import namedtuple
from config import api, sys, location, hw
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

    def __init__(self, connection, in_temp):
        logger.info("Reading forecast data")
        self._read1(connection)

        if api["variant"] == 2:
            self._read2_short(connection)
        else:
            self._read2_long(connection, 96)

        self._get_dht(in_temp)
        self._get_status()

    @staticmethod
    def _mk_id(id, rain):
        return id if id != 500 or rain < 2 else 520

    def _read1(self, connection):
        # Download hourly weather forecast for today
        url = "http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&APPID={}&mode=json&units={}&lang={}&exclude={}"
        fcast = connection.http_get_json(
            url.format(
                location["locations"][connection.config["location"]]["lat"],
                location["locations"][connection.config["location"]]["lon"],
                api["apikey"],
                api["units"],
                api["language"],
                "minutely,hourly,daily",
            )
        )

        # Parse todays forecast
        try:
            if not fcast["cod"] == 0:
                logger.info("Server commu8nication error - can not load forecast!")

                try:
                    logger.info("Server reported:")
                    logger.info("    ", fcast["message"])
                    logger.info("")
                    logger.info("Go into configuration mode to set server correctly")
                except:
                    ...

                play(
                    (400, 1000),
                    (200, 1000),
                    (400, 1000),
                    (200, 1000),
                    (400, 1000),
                    (200, 1000),
                )
                deepsleep()
        except:
            ...

        current = fcast["current"]

        try:
            rain = current["rain"]["1h"]
        except KeyError:
            rain = 0.0

        rpb = current.get("pop", 0) * 100

        try:
            snow = current["snow"]["1h"]
        except KeyError:
            snow = 0.0

        self.time_zone = fcast["timezone_offset"]

        weather = current["weather"][0]
        dsc = weather["description"]
        self.descr = dsc[0].upper() + dsc[1:]

        # Fix rain icon according to amount of rain
        def _mk_id(id, rain):
            return id if id != 500 or rain < 0.5 else 520

        self.weather = Forecast.Weather(
            "{}{}".format(
                id2icon[self._mk_id(weather["id"], rain)], weather["icon"][-1]
            ),
            current["dt"],
            current["sunrise"],
            current["sunset"],
            current["temp"],
            current["feels_like"],
            current["humidity"],
            rain,
            rpb,
            snow,
            current["wind_speed"],
            current["wind_deg"],
            current["clouds"],
        )
        self.time = Time(self.time_zone)

        # Set RTC clock according to forecast time
        rtc = RTC()
        dt = self.time.get_date_time(self.weather.dt)
        rtc.init((dt[0], dt[1], dt[2], 0, dt[3], dt[4], dt[5], 0))

    def _read2_short(self, connection):
        # Download hourly weather forecast for today
        url = "http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&APPID={}&mode=json&units={}&lang={}&exclude={}"
        fcast = connection.http_get_json(
            url.format(
                location["locations"][connection.config["location"]]["lat"],
                location["locations"][connection.config["location"]]["lon"],
                api["apikey"],
                api["units"],
                "EN",
                "current,minutely,daily",
            )
        )

        # Build 2 days forecast
        self.forecast = []
        self.step = 3600
        srt = self.weather.srt
        sst = self.weather.sst

        for current in fcast["hourly"]:
            weather = current["weather"][0]

            try:
                rain = current["rain"]["1h"]
            except KeyError:
                rain = 0.0

            rpb = current.get("pop", 0) * 100

            try:
                snow = current["snow"]["1h"]
            except KeyError:
                snow = 0.0

            dt = current["dt"]
            if dt > sst:
                srt += 86400
                sst += 86400

            id = (
                701
                if current["visibility"] < 500 and weather["id"] in range(800, 802)
                else weather["id"]
            )
            self.forecast.append(
                Forecast.Weather(
                    "{}{}".format(id2icon[self._mk_id(id, rain)], weather["icon"][-1]),
                    dt,
                    srt,
                    sst,
                    current["temp"],
                    current["feels_like"],
                    current["humidity"],
                    rain,
                    rpb,
                    snow,
                    current["wind_speed"],
                    current["wind_deg"],
                    current["clouds"],
                )
            )

    def _read2_long(self, connection, hours):
        # Download hourly weather forecast for 5 days
        url = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}&mode=json&units={}&lang={}&cnt={}"
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

            id = (
                701
                if current["visibility"] < 500 and weather["id"] in range(800, 802)
                else weather["id"]
            )
            self.forecast.append(
                Forecast.Weather(
                    "{}{}".format(id2icon[self._mk_id(id, rain)], weather["icon"][-1]),
                    dt,
                    srt,
                    sst,
                    main["temp"],
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

    def _get_dht(self, in_temp):
        # DHT22 is powered only when display is powered
        # (network is not connected)
        p = hw["pins"]["dht"]

        if p >= 0:
            sensor = dht.DHT22(Pin(p))

            try:
                sensor.measure()
                self.home = Forecast.Home(
                    sensor.temperature(),
                    sensor.humidity(),
                )
                return
            except:
                ...

        self.home = Forecast.Home(in_temp, None)
