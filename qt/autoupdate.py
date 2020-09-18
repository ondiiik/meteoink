def do_update(sha):
    from platform import IS_MICROPYTHON
    
    # Autoupdate only on ESP32 board
    if not IS_MICROPYTHON:
        return
    
#     from urequests import get
#     response = get('https://github.com/ondiiik/meteoink/raw/master/esp32/meteoink.fw')
#     print(response.content)
