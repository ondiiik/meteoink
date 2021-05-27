import                  dht
from machine     import Pin, deepsleep
from micropython import const
from collections import namedtuple
from config      import pins, sys, display_get, location, DISPLAY_JUST_REPAINT, VARIANT_2DAYS, DISPLAY_REFRESH_DIV, ui
from ltime       import Time
from uerrno      import ETIMEDOUT
from utime       import sleep_ms
from buzzer      import play
from log         import log


# See https://openweathermap.org/weather-conditions
id2icon = { 200 : '200', 201 : '200', 202 : '200', 210 : '200', 211 : '200', 212 : '200', 221 : '200', 230 : '200', 231 : '200', 232 : '200',
            300 : '300', 301 : '300', 302 : '300', 310 : '300', 311 : '300', 312 : '300', 313 : '300', 314 : '300', 321 : '300', 500 : '500',
            501 : '500', 502 : '500', 503 : '500', 504 : '500',
            511 : '511',
            520 : '520', 521 : '520', 522 : '520', 531 : '520',
            600 : '600', 601 : '600', 602 : '600', 611 : '600', 612 : '600', 613 : '600', 615 : '600', 616 : '600', 620 : '600', 621 : '600', 622 : '600',
            701 : '701', 711 : '701', 721 : '701', 731 : '701', 741 : '701', 751 : '701', 761 : '701', 762 : '701', 771 : '701', 781 : '701',
            800 : '800',
            801 : '801',
            802 : '802',
            803 : '803',
            804 : '804' }



class Forecast:
    Weather = namedtuple('Weather', ('id', 'dt', 'temp', 'feel', 'rh', 'rain', 'snow', 'speed', 'dir'))
    Home    = namedtuple('Home',    ('temp', 'rh'))
    
    
    def __init__(self, net, in_temp):
        log("Reading forecast data")
        self._read1(net, ui)
        
        if ui.variant == VARIANT_2DAYS:
            self._read2_short(net, ui)
        else:
            self._read2_long(net, ui, 96)
        
        self._get_dht(net, in_temp)
    
    
    def _read1(self, net, ui):
        if net is None:
            log('Reread current weather data ...')
            try:
                import owmp
                self.location = owmp.location
            except:
                deepsleep(1)
            
            fcast = owmp.current
        else:
            # Download hourly weather forecast for today
            log('Download current weather data ...')
            url   = 'http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&APPID={}&mode=json&units={}&lang={}&exclude={}'
            loc   = location[net.config.location]
            fcast = net.http_get_json(url.format(loc.lat,
                                                        loc.lon,
                                                        ui.apikey,
                                                        ui.units,
                                                        ui.language,
                                                        'minutely,hourly,daily'))
            
            with open('owmp.py', 'w') as f:
                f.write('location = "')
                f.write(loc.name)
                f.write('"\n')
                f.write('current = ')
                f.write(str(fcast))
                f.write('\n')
            
            return
        
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
        
        weather        = current['weather'][0]
        dsc            = weather['description']
        self.descr     = dsc[0].upper() + dsc[1:]
        
        self.weather   = Forecast.Weather(weather['id'],
                                          current['dt'],
                                          current['temp'],
                                          current['feels_like'],
                                          current['humidity'],
                                          rain,
                                          snow,
                                          current['wind_speed'],
                                          current['wind_deg'])
        self.time      = Time(self.time_zone)
    
    
    def _read2_short(self, connection, ui):
        if connection is None:
            log('Reread short weather data ...')
            import owmp
            fcast = owmp.forecast
        else:
            # Download hourly weather forecast for today
            log('Download short forecast data ...')
            
            url   = 'http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&APPID={}&mode=json&units={}&lang={}&exclude={}'
            fcast = connection.http_get_json(url.format(location[connection.config.location].lat,
                                                        location[connection.config.location].lon,
                                                        ui.apikey,
                                                        ui.units,
                                                        'EN',
                                                        'current,minutely,daily'))
            
            with open('owmp.py', 'a') as f:
                f.write('forecast = ')
                f.write(str(fcast))
                f.write('\n')
                
                return
        
        
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
            
            self.forecast.append(Forecast.Weather(701 if current['visibility'] < 500 and weather['id'] in range(800, 802) else weather['id'],
                                                  current['dt'],
                                                  current['temp'],
                                                  current['feels_like'],
                                                  current['humidity'],
                                                  rain,
                                                  snow,
                                                  current['wind_speed'],
                                                  current['wind_deg']))
    
    
    def _read2_long(self, connection, ui, hours):
        if connection is None:
            log('Reread long weather data ...')
            import owmp
            fcast = owmp.forecast
        else:
            # Download hourly weather forecast for 5 days
            log('Download long forecast data ...')
            url   = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}&mode=json&units={}&lang={}&cnt={}"
            fcast = connection.http_get_json(url.format(location[connection.config.location].lat,
                                                        location[connection.config.location].lon,
                                                        ui.apikey,
                                                        ui.units,
                                                        'EN',
                                                        (hours + 2) // 3))
            
            with open('owmp.py', 'a') as f:
                f.write('forecast = ')
                f.write(str(fcast))
                f.write('\n')
                
                return
        
        # Build 2 days forecast
        self.forecast = []
        
        for current in fcast['list']:
            main    = current['main']
            weather = current['weather'][0]
            wind    = current['wind']
            
            try:
                rain = current['rain']['3h']
            except KeyError:
                rain = 0.0
            
            try:
                snow = current['snow']['3h']
            except KeyError:
                snow = 0.0
            
            self.forecast.append(Forecast.Weather(701 if current['visibility'] < 500 and weather['id'] in range(800, 802) else weather['id'],
                                                  current['dt'],
                                                  main[   'temp'],
                                                  main[   'feels_like'],
                                                  main[   'humidity'],
                                                  rain,
                                                  snow,
                                                  wind[   'speed'],
                                                  wind[   'deg']))
    
    
    def _get_dht(self, net, in_temp):
        # DHT22 is powered only when display is powered
        # (network is not connected)
        if net is None and pins.DHT >= 0:
            sensor = dht.DHT22(Pin(pins.DHT))
            
            try:
                sensor.measure()
                self.home = Forecast.Home(sensor.temperature(), sensor.humidity() * sys.DHT_HUMI_CALIB[0] + sys.DHT_HUMI_CALIB[1])
                return
            except:
                pass
        
        self.home = Forecast.Home(in_temp, None)
