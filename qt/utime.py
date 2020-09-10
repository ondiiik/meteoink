def localtime(sec):
    import time
    return time.localtime(sec + 946677600)

def sleep_ms(ms):
    import time
    time.sleep(0.001 * ms)