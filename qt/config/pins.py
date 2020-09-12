from micropython import const

# Display related pins
SCK     = const(13)
MOSI    = const(14)
MISO    = const(12)

CS      = const(15)
DC      = const(27)
RST     = const(26)
BUSY    = const(25)

# DHT22 related pins
DHT     = const(22)

# Jumpers pins
HOTSPOT = const(16)
ALERT   = const(23)

# LED pin
LED     = const(2) 

# Battery voltage
VBAT    = const(32) 

# Battery voltage
BUZZER  = const(12) 