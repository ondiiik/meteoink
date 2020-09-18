from sys     import implementation
from jumpers import hotspot


if hotspot():
    # Don't use watchdog for hotspot (back doors)
    class WDT:
        def __init__(self, timeout):
            pass
        
        def feed(self):
            pass
else:
    # Use watchdog for station
    from machine import WDT


wdt = WDT(timeout = 7000)


if implementation.name == 'micropython':
    def refresh():
        wdt.feed()
        from gc import collect, threshold, mem_free, mem_alloc
        collect()
        threshold(mem_free() // 4 + mem_alloc())
else:
    def refresh():
        pass
