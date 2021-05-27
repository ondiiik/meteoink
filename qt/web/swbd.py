from config import alert


def page(web):
    if alert.error_beep:
        alert.error_beep = False
        alert.flush()
    
    return True
