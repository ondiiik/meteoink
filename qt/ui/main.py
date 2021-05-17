from .           import Ui
from config      import display_set, display_get, DISPLAY_REQUIRES_FULL_REFRESH, DISPLAY_JUST_REPAINT, DISPLAY_DONT_REFRESH
from display     import Vect, WHITE
from forecast    import TEMPERATURE, WEATHER, ALL
from micropython import const


_CHART_HEIGHT = const(90)


class Epd42(Ui):
    def __init__(self, canvas, forecast, connection):
        super().__init__(canvas)
        self.forecast   = forecast
        self.connection = connection
    
    
    def repaint_welcome(self, led):
        # Redraw display
        print('Drawing welcome ...')
        led.mode(led.DRAWING)
        
        bitmap = self.bitmap(1, 'greetings')
        self.canvas.bitmap(Vect(0, 0), bitmap)
        
        print('Flushing ...')
        led.mode(led.FLUSHING)
        self.canvas.flush()
    
    
    def repaint_weather(self, led, volt):
        # Redraw display
        print('Drawing weather ...')
        led.mode(led.DRAWING)
        
        self.canvas.fill(WHITE)
        
        if self.connection is None:
            # No forecast when there is no connection. Just draw no-wifi
            # symbol into middle of screen and leave
            bitmap  = self.bitmap(1, 'nowifi')
            self.canvas.bitmap(Vect(177, 0), bitmap)
        else:
            # We have forecast, so lets draw it on screen. Don't draw
            # always everything as forecast is changing not so often,
            # but temperature is.
            status = self.forecast.status
            
            if not status.refresh == TEMPERATURE:
                weather_dr(self, Vect(0,   0), Vect(960, 100))
                l = outside_dr(self, Vect(105, 0), Vect(295, 50))
            
            outtemp_dr(self, Vect(105, 0), Vect(295, 50))
            
            if status.refresh == ALL:
                cal_dr(self, Vect(0, 540 - 300 + 100), Vect(960, 26))
            
            if not status.refresh == TEMPERATURE:
                inside_dr(self, Vect(105, 50), Vect(295, 50), l, self.connection)
                vbat_dr(  self, Vect(284, 87), Vect(14, 10), volt)
                
            intemp_dr(self, Vect(105, 50), Vect(295, 50))
            
            if status.refresh == ALL:
                cal_dr(  self, Vect(0, 540 - 300 + 176), Vect(960, _CHART_HEIGHT + 5), False)
                tempg_dr(self, Vect(0, 540 - 300 + 176), Vect(960, _CHART_HEIGHT))
                icons_dr(self, Vect(0, 540 - 300 + 137), Vect(960, 40))
                wind_dr( self, Vect(0, 540 - 300 + 282), Vect(960, 20))
                rain_dr( self, Vect(0, 540 - 300 + 176), Vect(960, _CHART_HEIGHT))
                tempt_dr(self, Vect(0, 540 - 300 + 176), Vect(960, _CHART_HEIGHT))
        
        # Flush drawing on display (upper or all parts)
        print('Flushing ...')
        led.mode(led.FLUSHING)
        
        if self.connection is None:
            self.canvas.flush((180, 0, 32, 27))
        elif status.refresh == TEMPERATURE:
            self.canvas.flush((124, 0, 92, 98))
        elif status.refresh == WEATHER:
            self.canvas.flush((0, 0, 400, 98))
        else:
            self.canvas.flush()
        
        # Display is repainted, so next can be just partial repaint
        display_set(DISPLAY_JUST_REPAINT)
    
    
    def repaint_config(self, led, volt):
        from config.spot import hotspot
        
        # After config we will need to repaint all
        display_set(DISPLAY_REQUIRES_FULL_REFRESH)
        
        print('Drawing config ...')
        led.mode(led.DRAWING)
        self.canvas.fill(WHITE)
        
        qr_dr(self,
              Vect(0, 0),
              Vect(0, 0),
              ('WIFI:T:WPA;S:{};P:{};;'.format(hotspot.ssid, hotspot.passwd), 'WiFi', False));
        
        url = 'http://{}:5555'.format(self.connection.ifconfig[0])
        qr_dr(self, Vect(278, 178), Vect(0, 0), (url, 'Config URL', True));
        
        url_dr(self,  Vect(0,   self.canvas.dim.y // 2), Vect(self.canvas.dim.x - 132, self.canvas.dim.y // 2), url)
        wifi_dr(self, Vect(200, 0),                      Vect(self.canvas.dim.x - 132, self.canvas.dim.y // 2), hotspot)
        
        vbat_dr(self,  Vect(self.canvas.dim.x // 2 - 10, self.canvas.dim.y // 2),  Vect(20, 10), volt)
        
        print('Flushing ...')
        led.mode(led.FLUSHING)
        self.canvas.flush()
    
    
    def repaint_lowbat(self, volt):
        if not display_get() == DISPLAY_DONT_REFRESH:
            print('Drawing lowbat ...')
            self.canvas.fill(WHITE)
            v = Vect(self.canvas.dim.x // 2 - 30, self.canvas.dim.y // 2)
            d = Vect(60, 30)
            vbat_dr(self, v, d, volt)
            
            print('Flushing ...')
            self.canvas.flush((v.x - 20, v.y - 26, d.x + 46, d.y + 40))
            
            display_set(DISPLAY_DONT_REFRESH)
        else:
            print('Already painted ... saving battery')


def weather_dr(ui, p, d):
    from ui.weather import UiWeather
    UiWeather(p, d).repaint(ui)

def outside_dr(ui, p, d):
    from ui.outside import UiOutside
    return UiOutside(p, d).repaint(ui)

def outtemp_dr(ui, p, d):
    from ui.outtemp import UiOutTemp
    UiOutTemp(p, d).repaint(ui)

def inside_dr(ui, p, d, tab, connection):
    from ui.inside import UiInside
    UiInside(p, d).repaint(ui, (tab, connection))

def intemp_dr(ui, p, d):
    from ui.intemp import UiInTemp
    UiInTemp(p, d).repaint(ui)

def cal_dr(ui, p, d, title = True):
    from ui.calendar import UiCalendar
    UiCalendar(p, d).repaint(ui, title)

def icons_dr(ui, p, d):
    from ui.icons import UiIcons
    UiIcons(p, d).repaint(ui)

def rain_dr(ui, p, d):
    from ui.rain import UiRain
    UiRain(p, d).repaint(ui)

def tempg_dr(ui, p, d):
    from ui.tempg import UiTempGr
    UiTempGr(p, d).repaint(ui)

def wind_dr(ui, p, d):
    from ui.wind import UiWind
    UiWind(p, d).repaint(ui)

def tempt_dr(ui, p, d):
    from ui.tempt import UiTempTxt
    UiTempTxt(p, d).repaint(ui)

def fore_dr(ui, p, d):
    from ui.forecast import UiForecast
    UiForecast(p, d).repaint(ui)

def qr_dr(ui, p, d, a):
    from ui.qr import UiQr
    UiQr(p, d, a).repaint(ui)

def wifi_dr(ui, p, d, h):
    from ui.wifi import UiWifi
    UiWifi(p, d, h).repaint(ui)

def url_dr(ui, p, d, u):
    from ui.url import UiUrl
    UiUrl(p, d, u).repaint(ui)
    
def vbat_dr(ui, p, d, volt):
    from ui.vbat import UiVBat
    UiVBat(p, d).repaint(ui, volt)




class MeteoUi:
    def __init__(self, canvas, forecast, connection):
        self.ui              = Epd42(canvas, forecast, connection)
        self.repaint_welcome = self.ui.repaint_welcome
        self.repaint_weather = self.ui.repaint_weather
        self.repaint_config  = self.ui.repaint_config
        self.repaint_lowbat  = self.ui.repaint_lowbat

