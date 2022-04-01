from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run(b'264814939a0a66c9a966ac824584bf46b4d5726c')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
