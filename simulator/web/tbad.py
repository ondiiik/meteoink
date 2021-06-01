from config import alert


def page(web):
    if alert.temp_balanced:
        alert.temp_balanced = False
        alert.flush()
    
    yield web.index
