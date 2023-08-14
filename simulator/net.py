from ulogging import getLogger

logger = getLogger(__name__)
from gc import collect
from jumpers import jumpers
from micropython import const
from uerrno import ECONNRESET
import urequests
from db import location, connection, api


CONN_RETRY_CNT = const(6)


class Wifi:
    def __init__(self, ssid, bssid):
        self.ssid = ssid
        self.bssid = bssid


class Connection:
    def __init__(self):
        self.is_hotspot = False

        if jumpers.hotspot:
            logger.info('Setting hotspot by jumper')
            self.is_hotspot = True
        
        if not connection.CONNECTIONS:
            logger.warning('Forcing hotspot: Missing WiFi setup')
            self.is_hotspot = True
            
        if not location.LOCATIONS:
            logger.warning('Forcing hotspot: Missing Location')
            self.is_hotspot = True

        if not api.APIKEY:
            logger.warning('Forcing hotspot: Missing API key')
            self.is_hotspot = True

        if not self.is_hotspot:
            self.config = connection.CONNECTIONS[0]

        self.nets = [Wifi("mynet1", b"aaaaaa"), Wifi("mynet2", b"bbbbbb")]

    @property
    def ifconfig(self):
        return ("192.168.1.254", "255.255.255.0", "192.168.1.255")

    def http_get_json(self, url):
        logger.debug("HTTP GET: " + url)

        for retry in range(CONN_RETRY_CNT):
            try:
                return urequests.get(url).json()
                collect()
                return
            except OSError as font:
                logger.info("ECONNRESET -> retry")
                if font.errno == ECONNRESET:
                    continue

                raise font

    def disconnect(self):
        pass
