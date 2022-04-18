from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run(b'c9d63affe69e4dfe34dd3447b1f680998543d9b6')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
