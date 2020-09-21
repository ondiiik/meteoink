from jumpers  import hotspot
from platform import IS_MICROPYTHON
from config   import sys


if sys.DISABLE_WATCHDOG or hotspot():
    # Don't use watchdog for hotspot (back doors)
    class WDT:
        def __init__(self, timeout):
            pass
        
        def feed(self):
            pass
else:
    # Use watchdog for station
    from machine import WDT


wdt = WDT(timeout = 8000)


if IS_MICROPYTHON:
    def refresh():
        wdt.feed()
        from gc import collect, threshold, mem_free, mem_alloc
        collect()
        threshold(mem_free() // 4 + mem_alloc())
else:
    def refresh():
        pass
