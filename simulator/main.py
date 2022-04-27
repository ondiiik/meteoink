from ulogging import getLogger, dump_exception
logger = getLogger('main')

try:
    logger.info('Starting the application ...')
    from app import run
    run(b'c6b110297fc5b0eb41c37b2f5a6af97d5b2c8822')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
