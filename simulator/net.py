from ulogging import getLogger
logger = getLogger(__name__)
from gc import collect
from jumpers import jumpers
from micropython import const
from uerrno import ECONNRESET
import urequests
from config import connection, location, ui


CONN_RETRY_CNT = const(6)


class Wifi:
    def __init__(self, ssid, bssid):
        self.ssid = ssid
        self.bssid = bssid


class Connection:
    def __init__(self):
        self.is_hotspot = (jumpers.hotspot or 0 == len(connection) or 0 == len(location) or '' == ui.apikey)

        if not self.is_hotspot:
            self.config = connection[0]

        self.nets = [Wifi('mynet1', b'aaaaaa'), Wifi('mynet2', b'bbbbbb')]

    @property
    def ifconfig(self):
        return ('192.168.1.254', '255.255.255.0', '192.168.1.255')

    def http_get_json(self, url):
        logger.info("HTTP GET: " + url)

        for retry in range(CONN_RETRY_CNT):
            try:
                return urequests.get(url).json()
                collect()
                return
            except OSError as e:
                logger.info('ECONNRESET -> retry')
                if e.errno == ECONNRESET:
                    continue

                raise e

    def disconnect(self):
        pass
