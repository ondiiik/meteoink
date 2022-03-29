from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run(b'1268f3c2f72e71fe420895069491d64f2a655d28')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
