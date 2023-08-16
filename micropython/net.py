from ulogging import getLogger

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
        use_hotspot = False

        if jumpers.hotspot:
            logger.info("Setting hotspot by jumper")
            use_hotspot = True

        if not connection["connections"]:
            logger.warning("Forcing hotspot: Missing WiFi setup")
            use_hotspot = True

        if not location["locations"]:
            logger.warning("Forcing hotspot: Missing Location")
            use_hotspot = True

        if not api["apikey"]:
            logger.warning("Forcing hotspot: Missing API key")
            use_hotspot = True

        if use_hotspot:
            self._hotspot()
        else:
            self._attach()

    def _attach(self):
        # Activate WiFi interface
        logger.info(f"Connecting to WiFi ...")
        self._ifc = WLAN(STA_IF)

        if not self._ifc.active(True):
            raise RuntimeError("WiFi activation failed")

        # Search first based on BSSID
        network = None

        for n in self.nets:
            for c in connection["connections"]:
                if n.bssid == c["bssid"]:
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

    @property
    def ifconfig(self):
        return self._ifc.ifconfig()

    def http_get_json(self, url):
        logger.info(f"HTTP GET: {url}")

        for retry in range(CONN_RETRY_CNT):
            try:
                return urequests.get(url).json()
                collect()
                return
            except OSError as e:
                logger.warning("ECONNRESET -> retry")
                if e.errno == ECONNRESET:
                    continue

                raise e

    def disconnect(self):
        logger.info(f"Disconnecting from WiFi ...")
        WLAN(STA_IF).active(False)
        WLAN(AP_IF).active(False)
        self._ifc = None


def _bssid2bytes(bssid):
    b1 = bssid.split(":")
    b2 = []
    for i in range(6):
        b2.append(int(b1[i], 16))
    return bytes(b2)
