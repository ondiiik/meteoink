from usys       import print_exception
from config.sys import EXCEPTION_DUMP, VERBOSE_LOG
from buzzer     import play
from config     import alert
from machine    import RTC


try:
    _log = open('sys.log', 'a')
except:
    _log = open('sys.log', 'w')

_log.seek(0,2)


def dump_exception(msg, e):
    print(msg)
    print_exception(e)
    
    if EXCEPTION_DUMP > 0:
        pos = _log.tell()
        
        if pos < EXCEPTION_DUMP :
            dt  = RTC().datetime()
            _log.write(f'\n{dt[2]}.{dt[1]}.{dt[0]} {dt[4]}:{dt[5]:02} :: ')
            _log.write(msg)
            _log.write('\n')
            print_exception(e, _log)
            _log.flush()
    
    if alert.error_beep:
        play((200, 500), (100, 500))


if VERBOSE_LOG:
    def log(*args):
        print(*args)
        
        pos = _log.tell()
        
        if pos < EXCEPTION_DUMP:
            dt  = RTC().datetime()
            _log.write(f'{dt[2]}.{dt[1]}.{dt[0]} {dt[4]}:{dt[5]:02} ::')
            
            for s in args:
                _log.write(str(s))
            
            _log.write('\n')
            _log.flush()
else:
    log = print