from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame, Bitmap, V, Z, BLACK, WHITE, GREEN, BLUE, RED, YELLOW, ORANGE, ALPHA
from png import Reader
import math
import urequests
import gc
from framebuf import FrameBuffer, GS4_HMSB
from micropython import const
from io import BytesIO
from db import location, api, ui

_pow2 = 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608
_LEFT_OF = const(1)
_RIGHT_OF = const(2)
_ABOVE_OF = const(4)
_BELLOW_OF = const(8)


class RadarMap:
    _sides = (_LEFT_OF,               V(1,  0)), \
             (_LEFT_OF | _ABOVE_OF,   V(1,  1)), \
             (_ABOVE_OF,              V(0,  1)), \
             (_RIGHT_OF | _ABOVE_OF,  V(-1, 1)), \
             (_RIGHT_OF,              V(-1, 0)), \
             (_RIGHT_OF | _BELLOW_OF, V(-1, -1)), \
             (_BELLOW_OF,             V(0,  -1)), \
             (_LEFT_OF | _BELLOW_OF,  V(1,  -1))
    _swp_map0 = {True: BLUE, False: GREEN}
    _swp_map1 = {True: WHITE, False: GREEN}
    _swp_cld = {True: ALPHA, False: WHITE}

    def __init__(self, connection, wdt, dim, lat, lon, z):
        # Precalculate some useful values
        self.dim, self.dim2 = dim, dim // 2
        self.z = z
        self.map, self.origin = self._deg2tile(lat, lon, z)
        self.bitmap = Bitmap((dim.y, dim.x, bytearray(dim.x * dim.y // 2)))
        self.wdt = wdt

        # Load openstreet map
        path = f'bitmap/acep_rotated/map_{lat}_{lon}_{z}_{dim.x}_{dim.y}.bin'
        try:
            with open(path, 'rb') as f:
                f.readinto(self.bitmap.buf)
        except:
            crit0 = self._swp_map0
            crit1 = self._swp_map1
            self._load_file('https://stamen-tiles.a.ssl.fastly.net/toner/{}/{}/{}.png',
                            self.map.x,
                            self.map.y,
                            lambda a, n: crit1[a] if n[0] > 127 else crit0[a])
            with open(path, 'wb') as f:
                f.write(self.bitmap.buf)

        # Load clouds forecast
        crit = self._swp_cld
        self._load_file(f'https://tile.openweathermap.org/map/clouds_new/{{}}/{{}}/{{}}?appid={api.APIKEY}',
                        self.map.x,
                        self.map.y,
                        lambda a, n: crit[a] if n[3] > 64 else ALPHA)

        # Load rain forecast
        def scale(a, n):
            v = n[3]
            return ALPHA if v < 1 else crit[a] if v < 15 else GREEN if v < 25 else BLUE if v < 70 else ORANGE if v < 85 else RED
        self._load_file(f'https://tile.openweathermap.org/map/precipitation_new/{{}}/{{}}/{{}}?appid={api.APIKEY}', self.map.x, self.map.y, scale)

        # Maps are download - no other connection required
        connection.disconnect()

        # Mark center map point
        fb = self.bitmap.fb
        fb.fill_rect(self.dim2.y - 4, self.dim2.x - 4, 9, 9, ORANGE)
        fb.fill_rect(self.dim2.y - 2, self.dim2.x - 2, 5, 5, WHITE)

    def _load_file(self, fmt, x, y, conv, ofs=Z):
        # Load requested tile
        self.wdt.feed()
        url = fmt.format(self.z, x, y)
        logger.info(f'Loading {url} ...')
        imgstr = urequests.get(url)
        logger.info(f'Decoding PNG ...')
        width, height, data, meta = Reader(imgstr.content).read()
        gc.collect()

        missing = 0
        yofs = self.dim2.y - self.origin.y + ofs.y
        fb = self.bitmap.fb
        ww = self.dim.x
        logger.info(f'Drawing tile ...')
        for row, yy in zip(data, range(yofs, yofs + height)):
            if 0 > yy:
                missing |= _ABOVE_OF
            elif yy >= 256:
                missing |= _BELLOW_OF
            else:
                cv = bool(yy % 2)
                row = memoryview(row)
                xofs = self.dim2.x - self.origin.x + ofs.x
                for i, xx in zip(range(0, len(row), 4), range(xofs, xofs + width)):
                    if 0 > xx:
                        missing |= _LEFT_OF
                    elif xx >= 256:
                        missing |= _RIGHT_OF
                    else:
                        cv = not cv
                        c = conv(cv, row[i:i + 4])
                        if c != ALPHA:
                            fb.pixel(yy, ww - xx, c)

        # Load missing tiles
        if ofs != Z or 0 == missing:
            return

        pos = V(x, y)
        for mask, shift in self._sides:
            if (missing & mask) == mask:
                p = pos + shift
                o = shift * 256
                self._load_file(fmt, p.x, p.y, conv, o)

    @staticmethod
    def _deg2tile(lat, lon, z):
        lat_rad = math.radians(lat)
        n = _pow2[z]
        p = complex((lon + 180) / 360 * n,
                    (1 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2 * n)
        t = complex(int(p.real), int(p.imag))
        o = (p - t) * 256
        return V(int(t.real), int(t.imag)), V(int(o.real), int(o.imag))


class UiRadar(UiFrame):
    def draw(self, connection, wdt):
        wmap = RadarMap(connection,
                        wdt,
                        V(self.dim.x - 4, self.dim.y),
                        location.LOCATIONS[connection.config.location].lat,
                        location.LOCATIONS[connection.config.location].lon,
                        ui.SHOW_RADAR)

        self.canvas.bitmap(Z, wmap.bitmap)
        self.canvas.vline(V(self.dim.x - 4, 0), self.dim.y)
        self.canvas.hline(V(0, self.dim.y), self.canvas.dim.x)
