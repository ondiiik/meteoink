from log import dump_exception

try:
    print('Initializing watchdog ...')
    from machine import WDT
    wdt = WDT(timeout=120000)
    
    print('Starting the application ...')
    from app import run
    run(b'8ef390335a9b1fd58ee106c988f2617f6606ebe6')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
