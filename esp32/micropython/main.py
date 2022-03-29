from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run(b'c9d32117918ddfb52194937cb7fd88b4d5ca5015')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
