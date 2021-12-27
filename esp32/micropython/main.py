from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run(b'fdd04ce7a42b3005e4d722574315b654399707a7')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
