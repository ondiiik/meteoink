from usys       import print_exception
from config.sys import EXCEPTION_DUMP
from buzzer     import play
from config     import alert


def dump_exception(msg, e):
    print(msg)
    print_exception(e)
    
    if EXCEPTION_DUMP > 0:
        with open('sys.log', 'a') as log:
            pos = log.seek(0,2)
            
            if pos < EXCEPTION_DUMP :
                log.write('\n')
                log.write(msg)
                log.write('\n')
                print_exception(e, log)
    
    if alert.error_beep:
        play((200, 500), (100, 500))
