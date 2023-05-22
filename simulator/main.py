from ulogging import getLogger, dump_exception
logger = getLogger('main')

try:
    logger.info('Starting the application ...')
    from app import run
    run(b'bbe69d588f3215652c0cf532c1d6eaf9a0d89662')
    
except KeyboardInterrupt as e:
    logger.info('Interrupted by keyboard ...')
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
