from ulogging import getLogger, dump_exception
            logger = getLogger('main')
    
            try:
                logger.info('Starting the application ...')
                from app import run
                run(b'b11984f299d02b0f8b8d106453c53ed87f853e44')
                
            except KeyboardInterrupt as e:
                dump_exception('Interrupted by keyboard ...', e)
            except BaseException as e:
                dump_exception('!!! APPLICATION ERROR - REBOOTING !!!', e)
                import machine
                machine.reset()
            