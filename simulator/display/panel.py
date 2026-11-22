# Simulated display panel (PC simulator)
#
# Uses `ueink` driver without SPI only as frame buffer holder and displays
# its content in pygame window using palette provided by driver.
import pygame


class Panel:
    DRIVER = None  # ueink display driver class
    ROTATED = False  # Display is mounted rotated by 90 degrees (portrait)
    DEGHOST = False  # Clean display before each flush

    def __init__(self):
        self._epd = self.DRIVER()
        self.width, self.height = self.DRIVER.dim
        self._frame = 6

        # Display palette is mapped to all 16 frame buffer levels in the same
        # way as display does it (e.g. 3-color display shows any index >= 2
        # as its third color)
        pal = self.DRIVER.palette
        lut = [pal[min(i, len(pal) - 1)] for i in range(16)]
        self._pairs = [lut[b >> 4] + lut[b & 0x0F] for b in range(256)]

        w, h = (self.height, self.width) if self.ROTATED else (self.width, self.height)
        wsize = (w + self._frame * 2, h + self._frame * 2)

        self._screen = pygame.display.set_mode(wsize)
        pygame.draw.rect(self._screen, (127, 127, 127), [0, 0, *wsize])
        pygame.display.flip()

        self._clock = pygame.time.Clock()

        pygame.display.set_caption(
            f"EPD {self.width} x {self.height} - {self.DRIVER.__module__}"
        )

    def fb(self):
        return self._epd.buf

    def display_frame(self):
        pairs = self._pairs
        rgb = b"".join(pairs[b] for b in self._epd.buf)
        surface = pygame.image.frombuffer(rgb, (self.width, self.height), "RGB")

        if self.ROTATED:
            surface = pygame.transform.rotate(surface, -90)

        self._screen.blit(surface, (self._frame, self._frame))
        pygame.display.flip()
        self._clock.tick(2)

    def deghost(self): ...

    def deepsleep(self, t): ...
