from config import alert


def page(web):
    if not alert.error_beep:
        alert.error_beep = True
        alert.flush()
    
    return True
