# Measure chip temperature as soon as possible as chip is heating
from esp32 import raw_temperature

raw_temperature = raw_temperature()

# Now we can load the rest of system
from ulogging import getLogger, dump_exception

logger = getLogger(__name__)

from jumpers import jumpers
from net import Connection
from config import alert, display, beep, temp, vbat, behavior, hw, spot
from machine import deepsleep, reset, WDT, reset_cause, PWRON_RESET, Pin
from dht import DHT22
from battery import battery
from buzzer import play
from led import Led
from display import Canvas
from forecast import Forecast
from socket import socket, getaddrinfo
from ujson import dumps


def run():
    try:
        # Init all peripheries
        app = App()

        # It can happen that we want only to move meteostation somewhere
        # and don't want to let it wake up during transport. In this case
        # we can put it to greetings mode, where only picture is displayed
        # and station kept sleeping till reset button is pressed
        if display["greetings"] or jumpers.sleep:
            # Read all initializes all peripheries
            play((800, 30), 500, (400, 30))
            app.greetings()

        # It may happen that user wants to attach with HTTP for update of firmware
        # or configuration. In this case we can not rely on existing WiFi connection
        # and we rather go to hot-spot mode.
        if app.net and app.net.is_hotspot:
            if hw["variant"] == "epd47":
                app.hotspot_epd47()
            else:
                app.hotspot()

        # And finally - meteostation display - basic functionality ;-)
        else:
            # Checks if we will display RAW image from remote display server
            # or makes own meteostation screen based on openweathermap data.
            app.remote_display()

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
        dump_exception("FATAL - RECOVERY REQUIRED !!!", e)

        if beep["error_beep"]:
            play((200, 500), (100, 500))

        print("Going to emergency deep sleep for 5 minutes ...")
        deepsleep(5 * 60000)


class App:
    def __init__(self):
        # First of all we have to initialize watchdog if requested
        logger.info("Initializing watchdog ...")
        self.wdt = WDT(timeout=120000)

        # Try to read DHT sensor to get better temperature and humidity values.
        # Otherwise use at least less precise CPU temperature.
        try:
            p = hw["pins"]["dht"]
            if p >= 0:
                sensor = DHT22(Pin(p))
                sensor.measure()
                self.temp = sensor.temperature()
                self.rh = sensor.humidity()
            else:
                raise RuntimeError("No DHT")
        except:
            self.temp = ((raw_temperature() - 32) / 1.8) - 26.0
            self.rh = None

        # There is LED driver for debugging purposes. LED control
        # is running on background and can be disabled to save
        # piece of battery capacity. However then there is no
        # other way how to signalizes in which state meteostation
        # is then UART.
        self.led = Led()

        # Disable LED when battery voltage is too low
        self.volt = battery.voltage

        if self.volt < vbat["low_voltage"]:
            self.led.disable()

        # As we uses E-Ink display, the most comfortable way
        # how to work with it is to define canvas object for
        # drawing objects and flushing them later on screen.
        self.led.mode(Led.WARM_UP)
        self.canvas = Canvas()

        # When battery voltage is too low, just draw low battery
        # error on screen and go to deep sleep.
        if self.volt < vbat["low_voltage"]:
            logger.info("Low battery !!!")

            if not display.get("lowbat", False):
                self.net = None

                self.led.mode(Led.ALERT)

                from ui.main import MeteoUi

                ui = MeteoUi(self.canvas, None, None, self.led, self.wdt)
                ui.repaint_lowbat(self.volt)

                display["lowbat"] = True
                display.flush()

                self.sleep(30)  # Use EPD deep sleep to ensure to repaint display
            else:
                deepsleep(30 * 60000)  # Display is painted - just go to deep sleep

        else:
            display["lowbat"] = False
            display.flush()

        # Now we can create connection instance. Instance will not
        # connect immediately but only when it is needed as WiFi
        # heavily increase consumption of chip.
        self.led.mode(Led.DOWNLOAD)
        self.net = Connection()

    def greetings(self):
        from ui.main import MeteoUi

        ui = MeteoUi(self.canvas, None, self.net, self.led, self.wdt)
        ui.repaint_welcome()

        display["greetings"] = False
        display.flush()
        logger.info("Going to deep sleep ...")
        self.canvas.epd.deepsleep(0)

    def hotspot(self):
        play((2093, 30), 120, (2093, 30))
        self.led.mode(Led.DOWNLOAD)

        from ui.main import MeteoUi

        ui = MeteoUi(self.canvas, None, self.net, self.led, self.wdt)

        self.net.connect()
        ui.repaint_config(self.volt)

        self.web_server()

    def hotspot_epd47(self):
        if reset_cause() == PWRON_RESET:
            # EPD47 needs special handling as it have to draw screen and then
            # reboot to reach WiFi.
            play((2093, 30), 120, (2093, 30), 120, (2093, 30))
            self.led.mode(Led.DOWNLOAD)

            from ui.main import MeteoUi

            ui = MeteoUi(self.canvas, None, self.net, self.led, self.wdt)
            ui.repaint_config(self.volt)
            ui.canvas.epd.display_frame_now()

            deepsleep(1)
        else:
            # We are after deepsleep reset - screen is displayed,
            # so we can start server.
            play((2093, 30), 120, (2093, 30))
            self.net.connect()
            self.web_server()
            reset()

    def web_server(self):
        self.led.mode(Led.DOWNLOAD)

        logger.info("Loading module WEB")
        from web import WebServer

        server = WebServer(self.net, self.wdt)

        play((1047, 30), 120, (1319, 30), 120, (1568, 30), 120, (2093, 30))
        server.run()

        reset()

    def remote_display(self):
        display_port = behavior.get("display_port", 6625)

        if display_port == 0:
            return

        self.net.connect()
        address = self.net.config.get("remote_display", None)

        if address is None:
            return

        logger.info(f"Connecting to display server: {address}")

        try:
            logger.debug(f"Opening framebuff server at: 0.0.0.0:{display_port}")
            rs = socket()
            rs.bind(getaddrinfo("0.0.0.0", display_port)[0][-1])
            rs.listen(1)

            rq = socket()
            addr, port = address.split(":")
            port = int(port)
            rq.connect(getaddrinfo(addr, port)[0][-1])
            info = dumps(
                {
                    "id": spot["ssid"],
                    "port": display_port,
                    "display": {
                        "variant": hw["variant"],
                        "size": [self.canvas.width, self.canvas.height],
                        "rotation": self.canvas.rotation,
                    },
                    "sensors": {
                        "vbat": self.volt,
                        "temp": self.temp,
                        "rh": self.rh,
                    },
                }
            )
            logger.debug(f"Sending request: {info}")
            rq.sendall(info.encode())
            rq.close()

            cl, addr = rs.accept()
            r = len(self.canvas.buf)
            b = memoryview(self.canvas.buf)

            logger.debug("Receiving response ...")
            f = cl.makefile("rb", 0)

            minutes, _, _, _ = [i for i in f.read(4)]

            logger.debug("Receiving frame-buffer ...")
            while r:
                logger.debug(f"   remaining {r}B ...")
                r -= f.readinto(b[-r:])

            logger.debug(f"   remaining sleep time & flags ...")
            rs.close()

            logger.info(f"Frame buffer received")

            self.canvas.flush()
            self.sleep(minutes=minutes)

        except Exception as e:
            dump_exception(f"Unable to connect display server at {address}", e)

    def forecast(self):
        if self.net is None:
            return None
        else:
            self.net.connect()
            try:
                return Forecast(self.net, self.temp, self.rh)
            except OSError:
                return None

    def repaint(self, forecast):
        from ui.main import MeteoUi

        ui = MeteoUi(self.canvas, forecast, self.net, self.led, self.wdt)
        ui.repaint_forecast(self.volt)

    def allerts(self, forecast):
        # Is temperature balanced alert enabled?
        if not beep["temp_balanced"]:
            return

        # Is temperature outside lower then inside?
        if temp["indoor_high"] > forecast.home.temp:
            return

        # Do we measure during afternoon?
        h = forecast.time.get_date_time(forecast.weather.dt)[3]

        if h == 13:
            # Reset triggered flag in morning
            alert["already_triggered"] = False
            alert.flush()
            return

        # Didn't we already triggered alert?
        if (
            not alert["already_triggered"]
            and forecast.home.temp > forecast.weather.temp
        ):
            # Play alert and set that it has been triggered already
            for i in range(3):
                play(
                    (4000, 30),
                    (6000, 30),
                    (4000, 30),
                    (6000, 30),
                    (4000, 30),
                    (6000, 30),
                    (4000, 30),
                    (6000, 30),
                    500,
                )
            alert["already_triggered"] = True
            alert.flush()

    def sleep(self, forecast=None, minutes=0):
        if self.net is None:
            logger.info("No WiFi connection, retry in 5 minutes ...")
            self.canvas.epd.deepsleep(300000)

        if 0 == minutes:
            minutes = behavior["refresh"]
            h = (
                12
                if forecast is None
                else forecast.time.get_date_time(forecast.weather.dt)[3]
            )
            b, font = behavior["dbl"]

            if b > font:
                if h < font:
                    h += 24
                font += 24

            if h in range(b, font):
                minutes *= 2

        logger.info("Going to deep sleep for {} minutes ...".format(minutes))
        self.canvas.epd.deepsleep(minutes * 60000)
