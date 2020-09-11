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
    Weather     = namedtuple('Weather', ('id', 'dt', 'temp', 'feel', 'min', 'max', 'rh', 'rain', 'speed', 'dir'))
    Home        = namedtuple('Home',    ('temp', 'rh'))
    Status      = namedtuple('Status',  ('redraw', 'refresh', 'first'))
    
    WEATHER     = const(1)
    TEMPERATURE = const(2)
    ALL         = const(3)
    
    def __init__(self, connection, in_temp):
        print("Reading forecast data")
        from config import ui, pins
        from ltime import  Time
        
        url = "http://api.openweathermap.org/data/2.5/{}?q={},{}&APPID={}&mode=json&units={}&lang={}"
        
        # Download current weather situation
        weather = connection.http_get_json(url.format("weather",
                                                      connection.location,
                                                      connection.country,
                                                      ui.apikey,
                                                      ui.units,
                                                      ui.language))
        heap.refresh()
        
        try:
            r = weather['rain']['1h']
        except KeyError:
            r = 0.0
        
        m              = weather['main']
        e              = weather['weather'][0]
        w              = weather['wind']
        self.time_zone = weather['timezone']
        dsc            = e['description']
        self.descr     = dsc[0].upper() + dsc[1:]
        self.weather   = Forecast.Weather(e['id'], weather['dt'], m['temp'], m['feels_like'], m['temp_min'], m['temp_max'], m['humidity'], r, w['speed'], w['deg'])
        self.time      = Time(self.time_zone)
        
        
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
        
        # Refresh all once per 90 minutes
        ta = t % 90
        if (0 <= ta) and (ta < sleep_time):
            refresh = Forecast.ALL
        
        # Regardless on result - refresh all on first run
        try:
            open('~')
            first = False
        except:
            refresh = Forecast.ALL
            first   = True
        
        self.status = Forecast.Status(refresh, sleep_time, first)
        
        
        # Download weather forecast
        if refresh == Forecast.ALL:
            forecast = connection.http_get_json(url.format("forecast",
                                                           connection.location,
                                                           connection.country,
                                                           ui.apikey,
                                                           ui.units,
                                                           ui.language))
            connection.disconnect()
            heap.refresh()
            
            self.forecast = []
            
            for i in forecast['list']:
                m = i['main']
                e = i['weather'][0]
                w = i['wind']
                
                try:
                    r = i['rain']['3h']
                except KeyError:
                    r = 0.0
                
                self.forecast.append(Forecast.Weather(e['id'], i['dt'], m['temp'], m['feels_like'], m['temp_min'], m['temp_max'], m['humidity'], r, w['speed'], w['deg']))
        
        
        # And last is home temperature
        import              dht
        from machine import Pin
        
        try:
            sensor = dht.DHT22(Pin(pins.DHT))
            sensor.measure()
            self.home = Forecast.Home(sensor.temperature(), sensor.humidity())
        except OSError:
            self.home = Forecast.Home(in_temp, None)
