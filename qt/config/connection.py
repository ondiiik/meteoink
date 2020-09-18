from config import Connection


# Tuple containing connections and locations. Meteostation scan wifi
# and tries to connect to connect according to items in list..
#
# Format of connection description can be either based on SSID, e.g.:
#
#     Connection('Ben Nevis', 56.7968261, 5.0037003, 'my_wifi_name', 'my_great_password')
#
# But in the case that there is more stations in list with the same SSID,
# there can be used more uniq optional BSSID
#
#     Connection('Ben Nevis', 56.7968261, 5.0037003, 'my_wifi_name', 'my_great_password', b'\x01\x22\xF2\x55a\xef')
#
# When connection succeedes, then it load forecast for related location
connection = (Connection('Ben Nevis', 56.7968261, 5.0037003, 14.5217564, 'my_wifi_name', 'my_great_password'),)
