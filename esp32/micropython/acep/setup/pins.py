from micropython import const


# Display related pins
SCK = const(13)
MOSI = const(14)
MISO = const(12)

CS = const(15)
DC = const(27)
RST = const(26)
BUSY = const(25)

# DHT22 related pins
DHT = const(22)

# Jumpers pins
HOTSPOT_BUTTON = const(32)

# Alert toggle button pin
ALLERT_BUTTON = const(-1)

# Deep sleep button
SLEEP_BUTTON = const(-1)

# LED pin
LED = const(21)

# Battery voltage
VBAT = const(35)

# Battery voltage
BUZZER = const(33)
