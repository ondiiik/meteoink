from ulogging import getLogger, dump_exception
logger = getLogger('main')

try:
    logger.info('Starting the application ...')
    from app import run
    run(b'071656a9663cfe2b5119c00c1c31d8c77e0f2630')
    
except KeyboardInterrupt as e:
    dump_exception('Interrupted by keyboard ...', e)
except BaseException as e:
    dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
    import machine
    machine.reset()
