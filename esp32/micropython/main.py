from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run(b'59bda67cc80c31d0604493561181e0b22755e249')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
