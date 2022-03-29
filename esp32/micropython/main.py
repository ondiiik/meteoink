from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run(b'5f368ee606febaeeb63e53c7a4375429f0c6268d')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
