from jumpers import hotspot
from pyptf   import IS_MICROPYTHON
from config  import sys


if sys.WATCHDOG_TIME <= 0 or hotspot():
    # Don't use watchdog for hotspot (back doors)
    class WDT:
        def __init__(self, timeout):
            pass
        
        def feed(self):
            pass
else:
    # Use watchdog for station
    from machine import WDT


wdt = WDT(timeout = sys.WATCHDOG_TIME)

if IS_MICROPYTHON:
    def refresh():
        wdt.feed()
        from gc import collect, threshold, mem_free, mem_alloc
        collect()
        threshold(mem_free() // 4 + mem_alloc())
else:
    def refresh():
        pass
