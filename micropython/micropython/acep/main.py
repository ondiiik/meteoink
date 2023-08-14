from ulogging import getLogger, dump_exception

logger = getLogger("main")

try:
    logger.info("Starting the application ...")
    from app import run

    run()

except KeyboardInterrupt as e:
    dump_exception("Interrupted by keyboard ...", e)
except BaseException as e:
    dump_exception("!!! APPLICATION ERROR - REBOOTING !!!", e)
    import machine

    machine.reset()
