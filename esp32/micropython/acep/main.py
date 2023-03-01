from ulogging import getLogger, dump_exception
logger = getLogger('main')

try:
    logger.info('Starting the application ...')
    from app import run
    run(b'4e2ec13acf0962e6876a7783548fd51dee075c07')
    
except KeyboardInterrupt as e:
    logger.info('Interrupted by keyboard ...')
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
