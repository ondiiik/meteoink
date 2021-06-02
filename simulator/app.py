from var      import write, display
from var      import alert as alert_var
from battery  import battery
from buzzer   import play
from config   import alert, vbat, temp, DISPLAY_REQUIRES_FULL_REFRESH, DISPLAY_GREETINGS
from display  import Canvas
from esp32    import raw_temperature
from forecast import Forecast
from jumpers  import jumpers
from led      import Led
from machine  import deepsleep, reset, reset_cause, DEEPSLEEP
from net      import Connection
from ui.main  import MeteoUi
from log      import log, dump_exception
from web      import WebServer




def run(sha):
    try:
        # Beep when we are rebooted (only when this is not wake up
        # from deep sleep)
        if not DEEPSLEEP == reset_cause():
            play((2093, 30))
        
        
        # Read all initializes all peripheries
        temp, led, volt, canvas, net = _perif()
        
        
        # It can happen that we want only to move meteostation somewhere
        # and don't want to let it wake up during transport. In this case
        # we can put it to greetings mode, where only picture is displayed
        # and station kept sleeping till reset button is pressed
        if DISPLAY_GREETINGS == display.DISPLAY_STATE or jumpers.sleep:
            play((800, 30), 500, (400, 30))
            _greetings(canvas, net, led)
        
        
        # It may happen that user wants to attach with HTTP for update of firmware
        # or configuration. In this case we can not rely on existing WiFi connection
        # and we rather go to hot-spot mode.
        elif jumpers.hotspot:
            _hotspot(canvas, net, led, volt)
        
        # And finally - meteostation display - basic functionality ;-)
        else:
            # Network is running and connected ... we can checks for updates
            _update(net, sha)
            
            # Once we are connected to network, we can download forecast.
            # Just note that once forecast is download, WiFi is disconnected
            # to save as much battery capacity as possible.
            forecast = _forecast(net, temp)
            
            # Most time consuming part when we have all data is to draw them
            # on user interface - screen.
            _repaint(canvas, forecast, net, led, volt)
            
            # Forecast is painted. Now we shall checks for alerts if there are some
            # activated
            _allerts(forecast)
            
            # When all is displayed, then go to deep sleep. Sleep time is obtained
            # according to current weather forecast and UI needs and is in minutes.
            _sleep(net, forecast)
        
    except Exception as e:
        dump_exception('FATAL - RECOVERY REQUIRED !!!', e)
        _sleep(net, forecast, 5)



def _perif():
    # Reads internal temperature just after wake-up to reduce
    # influence of chip warm-up and use some kind of ambient
    # reduction to get more close to indoor temperature. This
    # value will be used when DTH22 or DHT11 sensor is
    # not found on selected pin.
    # 
    # Just note that better is to connect DHT22/DTH11 for
    # more precise temperature measurement and also for information
    # about humidity.
    temp = ((raw_temperature() - 32) / 1.8) - 26.0
    
    # There is LED driver for debugging purposes. LED control
    # is running on background and can be disabled to save
    # piece of battery capacity. However then there is no
    # other way how to signalizes in which state meteostation
    # is then UART.
    led = Led()
    
    # Disable LED when battery voltage is too low
    volt = battery.voltage
    
    if (volt < vbat.low_voltage):
        led.disable()
    
    
    # We shall checks if there is requested to toggle temperature alarm
    if jumpers.alert:
        alert.temp_balanced = not alert.temp_balanced
        
        if alert.temp_balanced:
            play((100, 50), (200, 50), (400, 50), (800, 50), (1600, 50), (3200, 50))
            write('alert', (False,))
        else:
            play((3200, 50), (1600, 50), (800, 50), (400, 50), (200, 50), (100, 50))
        
        alert.flush()
        deepsleep(1)
    
    
    # As we uses E-Ink display, the most comfortable way
    # how to work with it is to define canvas object for
    # drawing objects and flushing them later on screen.
    led.mode(Led.WARM_UP)
    canvas = Canvas()
    
        
    # When battery voltage is too low, just draw low battery
    # error on screen and go to deep sleep.
    if (volt < vbat.low_voltage):
        led.mode(Led.ALERT)
        
        ui = MeteoUi(canvas, None, None)
        ui.repaint_lowbat(volt)
        
        log('Low battery !!!')
        _sleep(15)
    
    # Once we have canvas established (large object needs
    # to be created first to prevent from memory fragmentation),
    # we can establish WiFi connection and connect to network.
    led.mode(Led.DOWNLOAD)
    
    net = None
    
    try:
        net = Connection()
        log('Connected to network')
    except Exception as e:
        dump_exception('Network connection error', e)
    
    
    return temp, led, volt, canvas, net



def _greetings(canvas, net, led):
    ui = MeteoUi(canvas, None, net)
    ui.repaint_welcome(led)
    
    write('display', (DISPLAY_REQUIRES_FULL_REFRESH,))
    log('Going to deep sleep ...')
    deepsleep()



def _hotspot(canvas, net, led, volt):
    play((2093, 30), 120,(2093, 30))
    led.mode(Led.DOWNLOAD)
    
    ui = MeteoUi(canvas, None, net)
    ui.repaint_config(led, volt)
    led.mode(Led.DOWNLOAD)
    
    server = WebServer(net)
    
    play((1047, 30), 120, (1319, 30), 120, (1568, 30), 120, (2093, 30))
    server.run()
    
    reset()



def _update(net, sha):
    pass
    # if sys.AUTOUPDATE and not net is None:
        # from autoupdate import do_update
        # do_update(sha)



def _forecast(net, temp):
    return None if net is None else Forecast(net, temp)



def _repaint(canvas, forecast, net, led, volt):
    ui = MeteoUi(canvas, forecast, net)
    ui.repaint_weather(led, volt)
    
    if not net is None:
        net = True



def _allerts(forecast):
    if not alert.temp_balanced:
        return
    
    if temp.indoor_high > forecast.home.temp:
        return
    
    h = forecast.time.get_date_time(forecast.weather.dt)[3]
    
    if h == 13:
        write('alert', (False,))
        return
    
    if not alert_var.ALREADY_TRIGGERED and forecast.home.temp > forecast.weather.temp:
        for i in range(3):
            play((4000, 30), (6000, 30), (4000, 30), (6000, 30), (4000, 30), (6000, 30), (4000, 30), (6000, 30), 500)
        write('alert', (True,))




def _sleep(net, fcast, minutes = 0):
    if net is None:
        log('No WiFi connection, retry in 5 minutes ...')
        deepsleep(300000)
    
    if 0 == minutes:
        from config import ui
        minutes = ui.refresh
        h       = 12 if fcast is None else fcast.time.get_date_time(fcast.weather.dt)[3]
        b, e    = ui.dbl
        
        if b > e:
            if h < e:
                h += 24
            e += 24
        
        if h in range(b, e):
            minutes *= 2
    
    
    log('Going to deep sleep for {} minutes ...'.format(minutes))
    deepsleep(minutes * 60000)
