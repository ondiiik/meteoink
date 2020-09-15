import                  heap
from collections import namedtuple
from micropython import const

# See https://openweathermap.org/weather-conditions
id2icon = { 200 : '200',
            201 : '200',
            202 : '200',
            210 : '200',
            211 : '200',
            212 : '200',
            221 : '200',
            230 : '200',
            231 : '200',
            232 : '200',
            300 : '300',
            301 : '300',
            302 : '300',
            310 : '300',
            311 : '300',
            312 : '300',
            313 : '300',
            314 : '300',
            321 : '300',
            500 : '500',
            501 : '500',
            502 : '500',
            503 : '500',
            504 : '500',
            511 : '511',
            520 : '520',
            521 : '520',
            522 : '520',
            531 : '520',
            600 : '600',
            601 : '600',
            602 : '600',
            611 : '600',
            612 : '600',
            613 : '600',
            615 : '600',
            616 : '600',
            620 : '600',
            621 : '600',
            622 : '600',
            701 : '701',
            711 : '701',
            721 : '701',
            731 : '701',
            741 : '701',
            751 : '701',
            761 : '701',
            762 : '701',
            771 : '701',
            781 : '701',
            800 : '800',
            801 : '801',
            802 : '802',
            803 : '803',
            804 : '804' }


class Forecast:
    Weather     = namedtuple('Weather', ('id', 'dt', 'temp', 'feel', 'rh', 'rain', 'speed', 'dir'))
    Home        = namedtuple('Home',    ('temp', 'rh'))
    Status      = namedtuple('Status',  ('refresh', 'sleep_time', 'first'))
    
    WEATHER     = const(1)
    TEMPERATURE = const(2)
    ALL         = const(3)
    
    def __init__(self, connection, in_temp):
        print("Reading forecast data")
        from config import ui
        
        if ui.variant == ui.VARIANT_2DAYS:
            fcast = self._read1_2days(connection)
        else:
            raise NotImplementedError('5 days not implemented yet')
        
        self._get_status(ui)
        
        if self.status.refresh == Forecast.ALL:
            if ui.variant == ui.VARIANT_2DAYS:
                self._read2_2days(fcast)
            else:
                raise NotImplementedError('5 days not implemented yet')
        
        self._get_dht(in_temp)
    
    
    def _read1_2days(self, connection):
        print("Reading forecast data")
        from config import ui
        from ltime  import Time
        
        # Download hourly weather forecast for 2 days
        url   = 'http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&APPID={}&mode=json&units={}&lang={}&exclude=minutely,daily'
        fcast = connection.http_get_json(url.format(connection.config.lat,
                                                    connection.config.lon,
                                                    ui.apikey,
                                                    ui.units,
                                                    ui.language))
        connection.disconnect()
        heap.refresh()
        
        # Parse todays forecast
        current = fcast['current']
        try:
            rain = current['rain']['1h']
        except KeyError:
            rain = 0.0
        
        self.time_zone = fcast['timezone_offset']
        
        weather        = current['weather'][0]
        dsc            = weather['description']
        self.descr     = dsc[0].upper() + dsc[1:]
        
        self.weather   = Forecast.Weather(weather['id'],
                                          current['dt'],
                                          current['temp'],
                                          current['feels_like'],
                                          current['humidity'],
                                          rain,
                                          current['wind_speed'],
                                          current['wind_deg'])
        self.time      = Time(self.time_zone)
        
        return fcast
    
    
    def _read2_2days(self, fcast):
        self.forecast = []
        
        for current in fcast['hourly']:
            weather = current['weather'][0]
            
            try:
                rain = current['rain']['3h']
            except KeyError:
                rain = 0.0
            
            self.forecast.append(Forecast.Weather(weather['id'],
                                                  current['dt'],
                                                  current['temp'],
                                                  current['feels_like'],
                                                  current['humidity'],
                                                  rain,
                                                  current['wind_speed'],
                                                  current['wind_deg']))
    
    
    def _get_status(self, ui):
        # Set forecast redraw status
        refresh = Forecast.TEMPERATURE
        
        dt = self.time.get_date_time(self.weather.dt)
        if (dt[3] < 6):
            sleep_time = 30
        else:
            sleep_time = 15
        
        # Once per 30 minutes refresh wather
        t  = (dt[3] * 60 + dt[4])
        
        ta = t % 30
        if (0 <= ta) and (ta < sleep_time):
            refresh = Forecast.WEATHER
        
        # Refresh all once per 90 or 60 minutes minutes
        ta = t % (60 if ui.variant == ui.VARIANT_2DAYS else 90)
        if (0 <= ta) and (ta < sleep_time):
            refresh = Forecast.ALL
        
        # Regardless on result - refresh all on first run
        try:
            open('~')
            first = False
        except:
            refresh = Forecast.ALL
            first   = True
        
        #sleep_time  = 3 # DEVEL - DEBUG
        self.status = Forecast.Status(refresh, sleep_time, first)
    
    
    def _get_dht(self, in_temp):
        import              dht
        from machine import Pin
        from config  import pins
        
        try:
            sensor = dht.DHT22(Pin(pins.DHT))
            sensor.measure()
            self.home = Forecast.Home(sensor.temperature(), sensor.humidity())
        except OSError:
            self.home = Forecast.Home(in_temp, None)
