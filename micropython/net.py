from ulogging import getLogger, dump_exception

logger = getLogger(__name__)

from jumpers import jumpers
from network import WLAN, STA_IF, AP_IF
from config import connection, location, spot, api
from utime import sleep
import urequests
from uerrno import ECONNRESET


CONN_RETRY_CNT = const(6)


class Wifi:
    def __init__(self, ssid, bssid):
        self.ssid = ssid
        self.bssid = bssid


class Connection:
    def __init__(self):
        self.is_hotspot = False
        self._ifc = None

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

    def connect(self):
        if self._ifc is not None:
            return

        try:
            # Scan networks in surrounding
            self._ifc = WLAN(STA_IF)

            if not self._ifc.active(True):
                raise RuntimeError("WiFi activation failed")

            sc = self._ifc.scan()
            self.nets = []

            for n in sc:
                self.nets.append(Wifi(n[0].decode(), n[1]))

            self._ifc.active(False)

            # Start requested variant of connection
            if self.is_hotspot:
                self._hotspot()
            else:
                self._attach()
            logger.info("Connected to network")

            type(self)._connected = True
        except Exception as font:
            self.net = None
            dump_exception("Network connection error", font)

            if beep["error_beep"]:
                play((200, 500), (100, 500))

            raise

    def disconnect(self):
        logger.info(f"Disconnecting from WiFi ...")
        WLAN(STA_IF).active(False)
        WLAN(AP_IF).active(False)
        self._ifc = None

    @property
    def ifconfig(self):
        return self._ifc.ifconfig()

    def http_get_json(self, url):
        logger.info(f"HTTP GET: {url}")

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

    def _attach(self):
        # Activate WiFi interface
        logger.info(f"Connecting to WiFi ...")
        self._ifc = WLAN(STA_IF)

        if not self._ifc.active(True):
            raise RuntimeError("WiFi activation failed")

        # Search first based on BSSID
        network = None

        for n in self.nets:
            bssid = bytes2bssid(n.bssid)
            for c in connection["connections"]:
                if bssid == c["bssid"]:
                    network = c
                    break
            else:
                continue
            break

        # Repeat the same for SSID if BSSID was not found
        if network is None:
            for n in self.nets:
                for c in connection["connections"]:
                    if n.ssid == c["ssid"]:
                        network = c
                        break
                else:
                    continue
                break

        # Checks if we have something and connect to WiFi
        if network is None:
            raise RuntimeError("No know WiFi found!")

        self.config = network

        self._ifc.connect(
            network["ssid"], network["passwd"], bssid=_bssid2bytes(network["bssid"])
        )

        for i in range(30):
            if self._ifc.isconnected():
                logger.info(f"Connected: {str(self.ifconfig)}")
                self.is_hotspot = False
                return

            logger.debug(f"Connecting ...")
            sleep(1)

        raise RuntimeError("Wifi connection refused")

    def _hotspot(self):
        # Create hotspot to be able to attach by FTP and configure meteostation
        self._ifc = WLAN(AP_IF)
        self._ifc.active(True)
        self._ifc.config(essid=spot["ssid"], password=spot["passwd"], authmode=3)

        while self._ifc.active() == False:
            sleep(1)

        self.is_hotspot = True
        logger.info(f"Running hotspot: {str(self.ifconfig)}")


def bytes2bssid(bssid):
    return ":".join("{:02X}".format(b) for b in bssid)


def _bssid2bytes(bssid):
    b1 = bssid.split(":")
    b2 = []
    for i in range(6):
        b2.append(int(b1[i], 16))
    return bytes(b2)
