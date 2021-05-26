from config import alert


def page(web):
    if not alert.temp_balanced:
        alert.temp_balanced = True
        alert.flush()
    
    return True
