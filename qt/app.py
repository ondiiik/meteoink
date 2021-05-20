from machine     import deepsleep, reset, reset_cause, DEEPSLEEP
from esp32       import raw_temperature
from config      import sys, display_set, display_get, DISPLAY_REQUIRES_FULL_REFRESH, DISPLAY_GREETINGS
from buzzer      import play
from config.vbat import VBAT_LOW
from battery     import battery
from led         import Led
from display     import Canvas
from net         import Connection
from jumpers     import jumpers
from forecast    import Forecast
from ui.main     import MeteoUi
from web.main    import WebServer



def run(sha):
    try:
        # initializes environment
        _init()
        
        # Read all initializes all peripheries
        temp, led, volt, canvas, net = _perif()
        print('perif ::', temp, led, volt, canvas, net)
        
        
        # It can happen that we want only to move meteostation somewhere
        # and don't want to let it wake up during transport. In this case
        # we can put it to greetings mode, where only picture is displayed
        # and station kept sleeping till reset button is pressed
        if DISPLAY_GREETINGS == display_get():
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
            _allerts()
            
            # When all is displayed, then go to deep sleep. Sleep time is obtained
            # according to current weather forecast and UI needs and is in minutes.
            _sleep(net, forecast)
        
    except Exception as e:
        from usys       import print_exception
        from config.sys import EXCEPTION_DUMP
        
        print_exception(e)
        
        if EXCEPTION_DUMP:
            with open('sys.log', 'a') as log:
                log.write('\n')
                print_exception(e, log)



def _init():
    # Beep when we are rebooted (only when this is not wake up
    # from deep sleep)
    if not DEEPSLEEP == reset_cause():
        play(((2093, 30),))
    
    # Checks if we are running right micropython firmware
    # This firmware expects some parts as built in, so the
    # exact firmware built ID to be present. Modules, which
    # is used for detection is pyptf (python platform).
    try:
        from pyptf import KERNEL_VARIANT
        
        if not 3 == KERNEL_VARIANT:
            raise RuntimeError()
    except:
        raise RuntimeError('''Incompatible micropython firmware found!
Please download right one here:
\t\thttps://github.com/ondiiik/meteoink/blob/master/esp32
''')



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
    
    if (volt < VBAT_LOW):
        led.disable()
    
    # As we uses E-Ink display, the most comfortable way
    # how to work with it is to define canvas object for
    # drawing objects and flushing them later on screen.
    led.mode(Led.WARM_UP)
    canvas = Canvas()
    
        
    # When battery voltage is too low, just draw low battery
    # error on screen and go to deep sleep.
    if (volt < VBAT_LOW):
        led.mode(Led.ALERT)
        
        ui = MeteoUi(canvas, None, None)
        ui.repaint_lowbat(volt)
        
        print('Going to deep sleep ...')
        deepsleep(120000)
    
    # Once we have canvas established (large object needs
    # to be created first to prevent from memory fragmentation),
    # we can establish WiFi connection and connect to network.
    led.mode(Led.DOWNLOAD)
    
    try:
        net = Connection()
    except Exception as e:
        print('Network connection reported', e)
        net = None
    
    
    return temp, led, volt, canvas, net



def _greetings(canvas, net, led):
    ui = MeteoUi(canvas, None, net)
    ui.repaint_welcome(led)
    
    print('Going to deep sleep ...')
    display_set(DISPLAY_REQUIRES_FULL_REFRESH)
    deepsleep()



def _hotspot(canvas, net, led, volt):
    play(((2093, 30), (0, 120),(2093, 30)))
    led.mode(Led.DOWNLOAD)
    
    ui = MeteoUi(canvas, None, net)
    ui.repaint_config(led, volt)
    led.mode(Led.DOWNLOAD)
    
    server = WebServer(net)
    
    play(((1047, 30), (0, 120), (1319, 30), (0, 120), (1568, 30), (0, 120), (2093, 30)))
    server.run()
    
    reset()



def _update(net, sha):
    if sys.AUTOUPDATE and not net is None:
        from autoupdate import do_update
        do_update(sha)



def _forecast(net, temp):
    return None if net is None else Forecast(net, temp)



def _repaint(canvas, forecast, net, led, volt):
    ui = MeteoUi(canvas, forecast, net)
    ui.repaint_weather(led, volt)
    
    if not net is None:
        net = True



def _allerts():
    pass



def _sleep(net, forecast):
    print('Going to deep sleep ...')
    if net is None:
        deepsleep(60000)
    else:
        deepsleep(forecast.status.sleep_time * 60000)
