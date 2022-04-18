print('Loading module SYSTEM')
from log import log, dump_exception
from net import Connection
from var import write, display
from var import alert as alert_var
from config import alert, vbat, temp, ui as ui_cfg, DISPLAY_REQUIRES_FULL_REFRESH, DISPLAY_GREETINGS
print('Loading module HW')
from machine import deepsleep, reset, reset_cause, DEEPSLEEP, WDT
from battery import battery
from buzzer import play
from esp32 import raw_temperature
from jumpers import jumpers
from led import Led
from display import Canvas
from forecast import Forecast
from ui.main import MeteoUi


def run(sha):
    try:
        # Init all peripheries
        app = App()

        # Beep when we are rebooted (only when this is not wake up
        # from deep sleep)
        if not DEEPSLEEP == reset_cause():
            play((2093, 30))

        # It can happen that we want only to move meteostation somewhere
        # and don't want to let it wake up during transport. In this case
        # we can put it to greetings mode, where only picture is displayed
        # and station kept sleeping till reset button is pressed
        if DISPLAY_GREETINGS == display.DISPLAY_STATE or jumpers.sleep:
            # Read all initializes all peripheries
            play((800, 30), 500, (400, 30))
            app.greetings()

        # It may happen that user wants to attach with HTTP for update of firmware
        # or configuration. In this case we can not rely on existing WiFi connection
        # and we rather go to hot-spot mode.
        elif jumpers.hotspot:
            app.hotspot()

        # And finally - meteostation display - basic functionality ;-)
        else:
            # Network is running and connected ... we can checks for updates
            app.update(sha)

            # Once we are connected to network, we can download forecast.
            # Just note that once forecast is download, WiFi is disconnected
            # to save as much battery capacity as possible.
            forecast = app.forecast()

            # Most time consuming part when we have all data is to draw them
            # on user interface - screen.
            app.repaint(forecast)

            # Forecast is painted. Now we shall checks for alerts if there are some
            # activated
            app.allerts(forecast)

            # When all is displayed, then go to deep sleep. Sleep time is obtained
            # according to current weather forecast and UI needs and is in minutes.
            app.sleep(forecast)

    except Exception as e:
        dump_exception('FATAL - RECOVERY REQUIRED !!!', e)
        app.sleep(forecast, 5)


class App:
    def __init__(self):
        # First of all we have to initialize watchdog if requested
        log('Initializing watchdog ...')
        self.wdt = WDT(timeout=120000)

        # Reads internal temperature just after wake-up to reduce
        # influence of chip warm-up and use some kind of ambient
        # reduction to get more close to indoor temperature. This
        # value will be used when DTH22 or DHT11 sensor is
        # not found on selected pin.
        #
        # Just note that better is to connect DHT22/DTH11 for
        # more precise temperature measurement and also for information
        # about humidity.
        self.temp = ((raw_temperature() - 32) / 1.8) - 26.0

        # There is LED driver for debugging purposes. LED control
        # is running on background and can be disabled to save
        # piece of battery capacity. However then there is no
        # other way how to signalizes in which state meteostation
        # is then UART.
        self.led = Led()

        # Disable LED when battery voltage is too low
        self.volt = battery.voltage

        if (self.volt < vbat.low_voltage):
            self.led.disable()

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
        self.led.mode(Led.WARM_UP)
        self.canvas = Canvas()

        # When battery voltage is too low, just draw low battery
        # error on screen and go to deep sleep.
        if (self.volt < vbat.low_voltage):
            self.led.mode(Led.ALERT)

            ui = MeteoUi(self.canvas, None, None)
            ui.repaint_lowbat(self.volt)

            log('Low battery !!!')
            self.sleep(15)

        # Once we have canvas established (large object needs
        # to be created first to prevent from memory fragmentation),
        # we can establish WiFi connection and connect to network.
        self.led.mode(Led.DOWNLOAD)

        try:
            self.net = Connection()
            log('Connected to network')
        except Exception as e:
            self.net = None
            dump_exception('Network connection error', e)

    def greetings(self):
        ui = MeteoUi(self.canvas, None, self.net)
        ui.repaint_welcome(self.led)

        write('display', (DISPLAY_REQUIRES_FULL_REFRESH,))
        log('Going to deep sleep ...')
        deepsleep()

    def hotspot(self):
        play((2093, 30), 120, (2093, 30))
        self.led.mode(Led.DOWNLOAD)

        ui = MeteoUi(self.canvas, None, self.net, self.led)
        ui.repaint_config(self.led, self.volt)
        self.led.mode(Led.DOWNLOAD)

        print('Loading module WEB')
        from web import WebServer
        server = WebServer(self.net, self.wdt)

        play((1047, 30), 120, (1319, 30), 120, (1568, 30), 120, (2093, 30))
        server.run()

        reset()

    def update(self, sha):
        pass
        # if sys.AUTOUPDATE and not net is None:
        # from autoupdate import do_update
        # do_update(sha)

    def forecast(self):
        return None if self.net is None else Forecast(self.net, self.temp)

    def repaint(self, forecast):
        ui = MeteoUi(self.canvas, forecast, self.net, self.led)
        ui.repaint_forecast(self.led, self.volt)

    def allerts(self, forecast):
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

    def sleep(self, forecast=None, minutes=0):
        if self.net is None:
            log('No WiFi connection, retry in 5 minutes ...')
            deepsleep(300000)

        if 0 == minutes:
            minutes = ui_cfg.refresh
            h = 12 if forecast is None else forecast.time.get_date_time(forecast.weather.dt)[3]
            b, e = ui_cfg.dbl

            if b > e:
                if h < e:
                    h += 24
                e += 24

            if h in range(b, e):
                minutes *= 2

        log('Going to deep sleep for {} minutes ...'.format(minutes))
        deepsleep(minutes * 60000)
