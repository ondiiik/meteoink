from ulogging import getLogger

logger = getLogger(__name__)

from gc import collect
from jumpers import jumpers
from micropython import const
from uerrno import ECONNRESET
import urequests
from config import location, connection, api


CONN_RETRY_CNT = const(6)


class Wifi:
    def __init__(self, ssid, bssid):
        self.ssid = ssid
        self.bssid = bssid


class Connection:
    def __init__(self):
        self.is_hotspot = False

        if jumpers.hotspot:
            logger.info("Setting hotspot by jumper")
            self.is_hotspot = True

        if not connection["connections"]:
            logger.warning("Forcing hotspot: Missing WiFi setup")
            self.is_hotspot = True

        if not location["locations"]:
            logger.warning("Forcing hotspot: Missing Location")
            self.is_hotspot = True

        if not api["apikey"]:
            logger.warning("Forcing hotspot: Missing API key")
            self.is_hotspot = True

        if not self.is_hotspot:
            self.config = connection["connections"][0]

        self.nets = [Wifi("mynet1", b"aaaaaa"), Wifi("mynet2", b"bbbbbb")]

    def connect(self):
        ...

    @property
    def ifconfig(self):
        return ("192.168.1.254", "255.255.255.0", "192.168.1.255")

    def http_get_json(self, url):
        logger.debug("HTTP GET: " + url)

        for _ in range(CONN_RETRY_CNT):
            try:
                return urequests.get(url).json()
                collect()
                return
            except OSError as e:
                if e.errno == ECONNRESET:
                    logger.warning("ECONNRESET -> retry")
                    continue
                logger.error(f"Connection error: {e}")
                ...
            except Exception as e:
                logger.error(f"Connection error: {e}")
                ...

        raise OSError("Page does not respond")

    def disconnect(self):
        ...


def bytes2bssid(bssid):
    return ":".join("{:02X}".format(b) for b in bssid)
