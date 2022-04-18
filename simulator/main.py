from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run(b'f593c9236712264bb1adac3edefa1aa32c8d1985')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
