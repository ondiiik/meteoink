from ulogging import getLogger
logger = getLogger(__name__)

from .. import UiFrame


class UiWArrow(UiFrame):
    def draw(self, weather, size=1):
        speed = weather.speed
        direction = weather.dir

        bitmap = self.ui.wind(size, speed, direction)
        pos = (self.dim - bitmap.dim) // 2
        self.canvas.bitmap(pos, bitmap)
