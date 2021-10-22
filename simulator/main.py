from log import dump_exception

try:
    print('Initializing watchdog ...')
    from machine import WDT
    wdt = WDT(timeout=120000)
    
    print('Starting the application ...')
    from app import run
    run(b'e933f67ec8729734657896441997d3b3c2a31321', wdt)
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
