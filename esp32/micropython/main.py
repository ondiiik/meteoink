from log import dump_exception

try:
    print('Starting the application ...')
    from app import run
    run(b'd9b7c83eef503f229f0b2391e4c325b2f2789958')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
