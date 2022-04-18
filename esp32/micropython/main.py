from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run(b'10d1f91b203b3ba2d7c4afb91a2159f3164ebfdc')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
