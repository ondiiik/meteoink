day_of_week = ("Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle")


_trn = {
    "Add new WiFi": "Přidat WiFi",
    "Add new location": "Přidat lokalitu",
    "Alerts": "Akustická upozornění",
    "Battery setup": "Nastavení baterie",
    "Cancel": "Zrušit",
    "Choose Language": "Zvolit jazyk (language)",
    "Choose WiFi to connect": "Vyberte WiFi síť",
    "Confort temperatures": "Konfortní teploty",
    "Critical voltage": "Kritické napětí (vybitá baterie)",
    "Current voltage": "Aktuální napětí",
    "DELETE CONNECTION": "SMAZAT WIFI PŘIPOJENÍ",
    "DELETE LOCATION": "SMAZAT LOKALITU",
    "Delete": "Smazat",
    "Disable": "Zakázat",
    "Display refresh time": "Časy překreslování displeje",
    "Doubled from": "Dvojitá doba - od",
    "Doubled to": "Dvojitá doba - do",
    "Edit API key": "Zadat API key",
    "Edit connection": "Upravit WiFi připojení",
    "Edit location": "Upravit lokalitu",
    "Edit temperatures": "Upravit teploty",
    "Edit": "Upravit",
    "Enable": "Povolit",
    "Four days": "Čtyřdenní",
    "GPS coordinates": "GPS souřadnice",
    "General setup": "Nastavení displeje",
    "Go to normal mode": "Zpět do režimu meteostanice",
    "Go to travel mode": "Zcela vypnout (opět zapnout tlačítkem reset)",
    "Hotspot SSID": "Nastavit název hotspotu",
    "Hotspot setup": "Nastavení hotspotu",
    "Ignore BSSID": "Ignorovat BSSID",
    "Indoor high": "Vnitřní nejvyšsí",
    "Language": "Jazyk (Language)",
    "Latitude": "Zem. šířka",
    "Location name": "Název místa",
    "Location": "Název místa",
    "Locations setup": "Nastavení lokalit",
    "Longitude": "Zem. délka",
    "Meteostation": "Meteostanice",
    "Misc": "Ostatní",
    "Name": "Název",
    "Outdoor high": "Venkovní nevvyšsí",
    "Outdoor low": "Venkovní nejnišsí",
    "Outside temperature balanced": "Vyrovnání vnitřní a vnější teploty",
    "Password": "Heslo",
    "Refresh time": "Četnost překreslování",
    "Set hotspot password": "Nastavit heslo pro hotspot",
    "Software bug detected": "Zjištěna softwarová chyba",
    "Submit": "Potvrdit",
    "Summer time": "Letní čas",
    "Two days": "Dvoudenní",
    "Units": "Jednotky",
    "Use with BSSID": "použít včetně BSSID",
    "Use": "Použít",
    "Variant": "Varianta",
    "WiFi setup": "Nastavení WiFi",
    "{} min (doubled from {}:00 to {}:00)": "{} min (mezi {}:00 a {}:00 dvakrát delší)",
}


def trn(eng):
    return _trn.get(eng, eng)
