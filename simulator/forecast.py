import dht
from machine import Pin, deepsleep, RTC
from micropython import const
from collections import namedtuple
from config import pins, sys, location, DISPLAY_JUST_REPAINT, VARIANT_2DAYS, DISPLAY_REFRESH_DIV, ui
from ltime import Time
from var import display
from buzzer import play
from log import log


# See https://openweathermap.org/weather-conditions
id2icon = {200: '200', 201: '200', 202: '200', 210: '200', 211: '200', 212: '200', 221: '200', 230: '200', 231: '200', 232: '200',
           300: '300', 301: '300', 302: '300', 310: '300', 311: '300', 312: '300', 313: '300', 314: '300', 321: '300', 500: '500',
           501: '500', 502: '500', 503: '500', 504: '500',
           511: '511',
           520: '520', 521: '520', 522: '520', 531: '520',
           600: '600', 601: '600', 602: '600', 611: '600', 612: '600', 613: '600', 615: '600', 616: '600', 620: '600', 621: '600', 622: '600',
           701: '701', 711: '701', 721: '701', 731: '701', 741: '701', 751: '701', 761: '701', 762: '701', 771: '701', 781: '701',
           800: '800',
           801: '801',
           802: '802',
           803: '803',
           804: '804'}


WEATHER = const(1)
TEMPERATURE = const(2)
ALL = const(3)


class Forecast:
    Weather = namedtuple('Weather', ('icon', 'dt', 'temp', 'feel', 'rh', 'rain', 'snow', 'speed', 'dir'))
    Home = namedtuple('Home',    ('temp', 'rh'))
    Status = namedtuple('Status',  ('refresh', 'sleep_time'))

    def __init__(self, connection, in_temp):
        print("Reading forecast data")
        self._read1(connection, ui)

        self._get_status(ui)

        if self.status.refresh == ALL:
            if ui.variant == VARIANT_2DAYS:
                self._read2_short(connection, ui)
            else:
                self._read2_long(connection, ui, 96)

        self._get_dht(in_temp)

    @staticmethod
    def _mk_id(id, rain):
        return id if id != 500 or rain < 2 else 520

    def _read1(self, connection, ui):
        # Download hourly weather forecast for today
        url = 'http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&APPID={}&mode=json&units={}&lang={}&exclude={}'
        fcast = connection.http_get_json(url.format(location[connection.config.location].lat,
                                                    location[connection.config.location].lon,
                                                    ui.apikey,
                                                    ui.units,
                                                    ui.language,
                                                    'minutely,hourly,daily'))

        # Parse todays forecast
        try:
            if not fcast['cod'] == 0:
                log('Server commu8nication error - can not load forecast!')

                try:
                    log('Server reported:')
                    log('    ', fcast['message'])
                    log('')
                    log('Go into configuration mode to set server correctly')
                except:
                    pass

                play((400, 1000), (200, 1000), (400, 1000), (200, 1000), (400, 1000), (200, 1000))
                deepsleep()
        except:
            pass

        current = fcast['current']

        try:
            rain = current['rain']['1h']
        except KeyError:
            rain = 0.0

        try:
            snow = current['snow']['1h']
        except KeyError:
            snow = 0.0

        self.time_zone = fcast['timezone_offset']

        weather = current['weather'][0]
        dsc = weather['description']
        self.descr = dsc[0].upper() + dsc[1:]

        # Fix rain icon according to amount of rain
        def _mk_id(id, rain):
            return id if id != 500 or rain < 0.5 else 520

        self.weather = Forecast.Weather('{}{}'.format(id2icon[self._mk_id(weather['id'], rain)], weather['icon'][-1]),
                                        current['dt'],
                                        current['temp'],
                                        current['feels_like'],
                                        current['humidity'],
                                        rain,
                                        snow,
                                        current['wind_speed'],
                                        current['wind_deg'])
        self.time = Time(self.time_zone)

        # Set RTC clock according to forecast time
        rtc = RTC()
        dt = self.time.get_date_time(self.weather.dt)
        rtc.init((dt[0], dt[1], dt[2], 0, dt[3], dt[4], dt[5], 0))

    def _read2_short(self, connection, ui):
        # Download hourly weather forecast for today
        url = 'http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&APPID={}&mode=json&units={}&lang={}&exclude={}'
        fcast = connection.http_get_json(url.format(location[connection.config.location].lat,
                                                    location[connection.config.location].lon,
                                                    ui.apikey,
                                                    ui.units,
                                                    'EN',
                                                    'current,minutely,daily'))
        connection.disconnect()

        # Build 2 days forecast
        self.forecast = []

        for current in fcast['hourly']:
            weather = current['weather'][0]

            try:
                rain = current['rain']['1h']
            except KeyError:
                rain = 0.0

            try:
                snow = current['snow']['1h']
            except KeyError:
                snow = 0.0

            id = 701 if current['visibility'] < 500 and weather['id'] in range(800, 802) else weather['id']
            self.forecast.append(Forecast.Weather('{}{}'.format(id2icon[self._mk_id(id, rain)], weather['icon'][-1]),
                                                  current['dt'],
                                                  current['temp'],
                                                  current['feels_like'],
                                                  current['humidity'],
                                                  rain,
                                                  snow,
                                                  current['wind_speed'],
                                                  current['wind_deg']))

    def _read2_long(self, connection, ui, hours):
        # Download hourly weather forecast for 5 days
        url = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}&mode=json&units={}&lang={}&cnt={}"
        fcast = connection.http_get_json(url.format(location[connection.config.location].lat,
                                                    location[connection.config.location].lon,
                                                    ui.apikey,
                                                    ui.units,
                                                    'EN',
                                                    (hours + 2) // 3))
        connection.disconnect()

        # Build 2 days forecast
        self.forecast = []

        for current in fcast['list']:
            main = current['main']
            weather = current['weather'][0]
            wind = current['wind']

            try:
                rain = current['rain']['3h']
            except KeyError:
                rain = 0.0

            try:
                snow = current['snow']['3h']
            except KeyError:
                snow = 0.0

            id = 701 if current['visibility'] < 500 and weather['id'] in range(800, 802) else weather['id']

            self.forecast.append(Forecast.Weather('{}{}'.format(id2icon[self._mk_id(id, rain)], weather['icon'][-1]),
                                                  current['dt'],
                                                  main['temp'],
                                                  main['feels_like'],
                                                  main['humidity'],
                                                  rain,
                                                  snow,
                                                  wind['speed'],
                                                  wind['deg']))

    def _get_status(self, ui):
        # Set forecast redraw status
        refresh = TEMPERATURE

        dt = self.time.get_date_time(self.weather.dt)
        if (dt[3] < 6):
            sleep_time = 30
        else:
            sleep_time = 30 // DISPLAY_REFRESH_DIV

        # Once per 30 minutes refresh wather
        t = (dt[3] * 60 + dt[4])

        ta = t % 30
        if (0 <= ta) and (ta < sleep_time):
            refresh = WEATHER

        # Refresh all once per 90 or 60 minutes minutes
        ta = t % (60 if ui.variant == VARIANT_2DAYS else 90)
        if (0 <= ta) and (ta < sleep_time):
            refresh = ALL

        # Regardless on result - refresh all on first run
        if not display.DISPLAY_STATE == DISPLAY_JUST_REPAINT:
            refresh = ALL

        self.status = Forecast.Status(refresh, sleep_time)

    def _get_dht(self, in_temp):
        # DHT22 is powered only when display is powered
        # (network is not connected)
        if pins.DHT >= 0:
            sensor = dht.DHT22(Pin(pins.DHT))

            try:
                sensor.measure()
                self.home = Forecast.Home(sensor.temperature(), sensor.humidity() * sys.DHT_HUMI_CALIB[0] + sys.DHT_HUMI_CALIB[1])
                return
            except:
                pass

        self.home = Forecast.Home(in_temp, None)
