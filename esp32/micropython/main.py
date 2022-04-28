from ulogging import getLogger, dump_exception
logger = getLogger('main')

try:
    logger.info('Starting the application ...')
    from app import run
    run(b'5e0da8768a9d8d36ca930461f5e785a8c3396b97')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
