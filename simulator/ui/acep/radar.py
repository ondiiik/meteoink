from ulogging import getLogger

logger = getLogger(__name__)

from ui import (
    UiFrame,
    Bitmap,
    Vect,
    ZERO,
)
from display.epd import ALPHA, BLACK, BLUE, GREEN, ORANGE, RED, WHITE
from png import Reader
import math
import micropython
import urequests
import gc
from array import array
from micropython import const
from config import location, api, behavior
from version import VERSION

_HEADERS = {"User-Agent": f"Meteoink/{VERSION} (https://github.com/ondiiik/meteoink)"}

_pow2 = (
    1,
    2,
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    512,
    1024,
    2048,
    4096,
    8192,
    16384,
    32768,
    65536,
    131072,
    262144,
    524288,
    1048576,
    2097152,
    4194304,
    8388608,
)
_LEFT_OF = const(1)
_RIGHT_OF = const(2)
_ABOVE_OF = const(4)
_BELLOW_OF = const(8)


@micropython.viper
def _draw_row(dst: ptr8, src: ptr8, lut: ptr8, prm: ptr32):
    """Draw one tile row into transposed GS4_HMSB bitmap through color LUT

    LUT has 2 x 256 entries - first half for odd, second for even checkerboard
    fields, indexed by key byte of pixel (palette index or alpha).

    prm = (k_lo, k_hi, planes, key_ofs, xofs, yy, ww, fb_stride)
    """
    k_lo = prm[0]
    k_hi = prm[1]
    planes = prm[2]
    key_ofs = prm[3]
    xofs = prm[4]
    yy = prm[5]
    ww = prm[6]
    half = prm[7] >> 1
    col = yy >> 1
    odd = yy & 1

    for k in range(k_lo, k_hi):
        xx = xofs + k
        c = int(lut[((((xx + yy) & 1) ^ 1) << 8) | int(src[k * planes + key_ofs])])
        if c != 7:  # ALPHA
            o = (ww - xx) * half + col
            if odd:
                dst[o] = (int(dst[o]) & 0xF0) | c
            else:
                dst[o] = (int(dst[o]) & 0x0F) | (c << 4)


class RadarMap:
    _sides = (
        (_LEFT_OF, Vect(1, 0)),
        (_LEFT_OF | _ABOVE_OF, Vect(1, 1)),
        (_ABOVE_OF, Vect(0, 1)),
        (_RIGHT_OF | _ABOVE_OF, Vect(-1, 1)),
        (_RIGHT_OF, Vect(-1, 0)),
        (_RIGHT_OF | _BELLOW_OF, Vect(-1, -1)),
        (_BELLOW_OF, Vect(0, -1)),
        (_LEFT_OF | _BELLOW_OF, Vect(1, -1)),
    )
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
        path = f"bitmaps/map_{lat}_{lon}_{z}_{dim.x}_{dim.y}.bin"
        try:
            with open(path, "rb") as f:
                f.readinto(self.bitmap.buf)
        except:
            crit0 = self._swp_map0
            crit1 = self._swp_map1
            self._load_file(
                "https://tile.openstreetmap.org/{}/{}/{}.png",
                self.map.x,
                self.map.y,
                lambda a, n: crit1[a] if ((abs(n[0]-0x9B) + abs(n[1] - 0x9D) + abs(n[2] - 0xA3)) > 72) else crit0[a],
                # store_png=True,
            )
            with open(path, "wb") as f:
                f.write(self.bitmap.buf)

        # Load clouds forecast
        crit = self._swp_cld
        # self._load_file(
        #     f"https://tile.openweathermap.org/map/clouds_new/{{}}/{{}}/{{}}?appid={api['apikey']}",
        #     self.map.x,
        #     self.map.y,
        #     lambda a, n: crit[a] if n[3] > 64 else ALPHA,
        # )

        # Load rain forecast
        def scale(a, n):
            v = n[3]
            return (
                ALPHA
                if v < 1
                else (
                    crit[a]
                    if v < 15
                    else (
                        GREEN
                        if v < 25
                        else BLUE if v < 70 else ORANGE if v < 85 else RED
                    )
                )
            )

        self._load_file(
            f"https://tile.openweathermap.org/map/precipitation_new/{{}}/{{}}/{{}}?appid={api['apikey']}",
            self.map.x,
            self.map.y,
            scale,
            alpha_only=True,
        )

        # Maps are download - no other connection required
        connection.disconnect()

        # Mark center map point
        fb = self.bitmap.fb
        fb.fill_rect(self.dim2.y - 4, self.dim2.x - 4, 9, 9, BLACK)
        fb.fill_rect(self.dim2.y - 2, self.dim2.x - 2, 5, 5, WHITE)

    def _load_file(self, fmt, x, y, conv, ofs=ZERO, store_png=False, alpha_only=False):
        """Load map tile and draw it into bitmap

        :param conv:        Converts `(checkerboard, pixel)` to display color.
        :param alpha_only:  `conv` uses only alpha channel of pixel (`pixel[3]`),
                            which allows to use fast LUT drawing also for RGBA tiles.
        """
        # Load requested tile
        self.wdt.feed()
        url = fmt.format(self.z, x, y)
        logger.info(f"Loading {url} ...")
        if store_png:
            fname = url.replace(".png", "~png").replace(":", "_").replace("/", "_").replace("?", "_").replace("=", "_").replace(".", "_").replace("~png", ".png")
            try:
                with open(fname, "rb") as f:
                    img = f.read()
                    logger.debug(f"Reusing {fname}")
            except Exception:
                logger.debug(f"Downloading {fname}")
                img = urequests.get(url, headers=_HEADERS).content
                with open(fname, "wb") as f:
                    f.write(img)
        else:
            img = urequests.get(url, headers=_HEADERS).content
        logger.debug(f"Decoding PNG ...")
        width, height, data, meta = Reader(img).read()
        img = None
        planes = meta["planes"]
        palette = meta.get("palette", None)

        gc.collect()

        xofs = self.dim2.x - self.origin.x + ofs.x
        yofs = self.dim2.y - self.origin.y + ofs.y
        fb = self.bitmap.fb
        ww = self.dim.x
        fbw, fbh = self.dim.y, self.dim.x  # Bitmap is transposed (x -> rows)

        # Which neighbor tiles are needed to cover whole area
        missing = 0
        if yofs < 0:
            missing |= _ABOVE_OF
        if yofs + height > 256:
            missing |= _BELLOW_OF
        if yofs < 256 and yofs + height > 0:
            if xofs < 0:
                missing |= _LEFT_OF
            if xofs + width > 256:
                missing |= _RIGHT_OF

        # Range of tile columns which are visible in bitmap. Column `k` is drawn
        # to pixel `(yy, ww - xx)` where `xx = xofs + k`.
        k_lo = max(0, -xofs, ww - fbh + 1 - xofs)
        k_hi = min(width, 256 - xofs, ww + 1 - xofs)
        y_end = min(256, fbw)

        # Fast path - color depends only on single byte of pixel (palette index
        # or alpha channel), so conversion can be precomputed into LUT
        lut = None
        if palette:
            lut = bytearray(512)
            for i, n in enumerate(palette):
                lut[i] = conv(False, n)
                lut[256 + i] = conv(True, n)
            key_ofs = 0
        elif alpha_only and meta["bitdepth"] == 8 and meta["alpha"]:
            lut = bytearray(512)
            for i in range(256):
                n = (0, 0, 0, i)
                lut[i] = conv(False, n)
                lut[256 + i] = conv(True, n)
            key_ofs = planes - 1

        logger.debug(f"Drawing tile ...")
        if lut is not None and k_lo < k_hi:
            buf = self.bitmap.buf
            stride = (fbw + 1) & ~1  # GS4_HMSB rows are aligned to whole bytes
            prm = array("i", (k_lo, k_hi, planes, key_ofs, xofs, 0, ww, stride))
            for r, row in enumerate(data):
                yy = yofs + r
                if yy >= y_end:
                    break  # Rest of tile is not visible - no need to decode it
                if yy >= 0:
                    prm[5] = yy
                    _draw_row(buf, row, lut, prm)
        elif k_lo < k_hi:
            # Generic (slow) path
            for r, row in enumerate(data):
                yy = yofs + r
                if yy >= y_end:
                    break
                if yy < 0:
                    continue
                for k in range(k_lo, k_hi):
                    xx = xofs + k
                    cv = not ((xx + yy) & 1)
                    n = palette[row[k]] if palette else row[k * planes : k * planes + planes]
                    c = conv(cv, n)
                    if c != ALPHA:
                        fb.pixel(yy, ww - xx, c)

        data = None
        gc.collect()

        # Load missing tiles
        if ofs != ZERO or 0 == missing:
            return

        pos = Vect(x, y)
        for mask, shift in self._sides:
            if (missing & mask) == mask:
                p = pos + shift
                o = shift * 256
                self._load_file(fmt, p.x, p.y, conv, o, store_png, alpha_only)

    @staticmethod
    def _deg2tile(lat, lon, z):
        lat_rad = math.radians(lat)
        n = _pow2[z]
        p = complex(
            (lon + 180) / 360 * n,
            (1 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)
            / 2
            * n,
        )
        t = complex(int(p.real), int(p.imag))
        o = (p - t) * 256
        return Vect(int(t.real), int(t.imag)), Vect(int(o.real), int(o.imag))


class UiRadar(UiFrame):
    def draw(self, connection, wdt):
        wmap = RadarMap(
            connection,
            wdt,
            Vect(self.dim.x - 4, self.dim.y),
            location["locations"][connection.config["location"]]["lat"],
            location["locations"][connection.config["location"]]["lon"],
            behavior["show_radar"],
        )

        self.canvas.bitmap(ZERO, wmap.bitmap)
        self.canvas.vline(Vect(self.dim.x - 4, 0), self.dim.y)
        self.canvas.hline(Vect(0, self.dim.y), self.canvas.dim.x)
