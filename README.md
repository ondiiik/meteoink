# Meteoink

![EPD 5.65 ACEP inch meteostation](graphics/doc/meteostation_acep.jpeg "EPD 5.65 ACEP inch meteostation")
![EPD 4.2 inch meteostation](graphics/doc/meteostation.jpeg "EPD 4.2 inch meteostation")


## What Meteoink is

Meteoink is home meteostation based on [4.2 inch dual color E-Ink display](https://www.waveshare.com/4.2inch-e-paper-module-c.htm) (BWY variant)
or [5.65 inch 7 colors E-Ink display](https://www.waveshare.com/5.65inch-e-paper-module-f.htm) (ACEP variant),
[TTGO-T8-ESP32](https://github.com/LilyGO/TTGO-T8-ESP32) and [micropython 1.20](https://micropython.org/). Meteostation
is connected to your home WiFi and uses data from [OpenWeatherMap](https://openweathermap.org/) project for obtaining
weather forecast. It also uses [DHT22](https://github.com/semestrinis/Arduino/wiki/DHT22-temperature-humidity-sensor)
sensor for measuring indoor temperature and humidity. Whole system is powered from one
[18650 Li-On battery](https://en.wikipedia.org/wiki/List_of_battery_sizes#Lithium-ion_batteries_(rechargeable))
charged through the USB on ESP board. Meteostation is usually operating half a year when refresh time is set to
20 minutes and there is good internet WiFi access.


## Wiring

![Meteostation wiring](graphics/doc/wiring.png "Meteostation wiring")

Some pins can be moved to another position by changing config file [pins.py](https://github.com/ondiiik/meteoink/blob/master/esp32/micropython/acep/setup/pins.py).

but keep in mind that not all pins are available for any operation (some are not capable of ADC, some are not capable of SPI, ...).
Also battery is not displayed in wiring as it has its own connector so its connection is obvious.


## Box

Files for 3D printed parts are stored [here](https://github.com/ondiiik/meteoink/tree/master/box).

Both variants of box are partialy screwed and partially glued as well as electronics. To stitch processor board or battery
you can use acrylate 3M double side tape. DHT22 sensor is glued to chassis (grid for air access shall be on the side pointing
outside the box). When you glue it, apply glue very carefully as it shall not pass inside electronics
(especially in the case of buttons or DHT sensor). When all electronics is inside, then chassis shall be either glued to frame
(BWY variant) or screwed together (ACEP variant).

### BWY (EPD 4.2)

![3D printed frame](graphics/doc/frame03.jpeg "3D printed frame")
![3D printed frame](graphics/doc/frame02.jpeg "3D printed frame")
![3D printed frame](graphics/doc/frame01.jpeg "3D printed frame")

### ACEP (EPD 5.65)

![3D printed frame](graphics/doc/frame11.jpeg "3D printed frame")
![3D printed frame](graphics/doc/frame12.jpeg "3D printed frame")
![3D printed frame](graphics/doc/frame13.jpeg "3D printed frame")
![3D printed frame](graphics/doc/frame14.jpeg "3D printed frame")


## Micropython

To make software running on ESP32, you have to install Micropython first on it. You shall use
[custom built of Micropython](https://github.com/ondiiik/meteoink/blob/master/esp32/micropython.bin)
according to [this tutorial](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html#deploying-the-firmware).
The reason for custom build is, that startup of meteostation is then way faster. This significantly reduce battery consumption.
You can also use [thonny IDE](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/) to do
this job for you.


## Upload binary files

The last step is to upload required binary files into device file sytem. This binaries are located in repository folder
[esp32/micropython](https://github.com/ondiiik/meteoink/tree/master/esp32/micropython) for each variant of display. There is [esp32/micropython/bwy](https://github.com/ondiiik/meteoink/tree/master/esp32/micropython/bwy)
folder for 4.2 inch Black/White/Yellow display, or [esp32/micropython/acep](https://github.com/ondiiik/meteoink/tree/master/esp32/micropython/acep)
folder for 5.65 7-color ACEP display. All files from selected folder shall be copied into board.
For this purpose REPL based file access engine such as [ampy](https://techtutorialsx.com/2017/06/04/esp32-esp8266-micropython-uploading-files-to-the-file-system/) or
[thonny IDE](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/) can be used for writing files into file system.
Just keep in mind that you shall be disconnected from console otherwise this tools will not work properly.


## Configuration - first run

With first run the metostation automatically switch to WiFi AP mode. You can use QR codes displayed on screen to setup your mobile phone WiFi and open suitable WEB page.

![Initial screen](graphics/doc/initial.png "Initial screen")

Once you are connected to meteostation, you shall see webpage similar to this one:

![Config web page](graphics/doc/config.png "Config web page")

To make station into operation you have to do following steps:

### Add your location

You shall add at least one location at the beginning. This location will be later used in WiFi configuration.
You can use more locations and bind them later to various WiFi, so when you are taking your weather station on holiday,
it choose location according to WiFi in your location.

### Add WiFi

Next step is to connect WiFi. When you attempt to connect WiFi, the list of available networks will be displayed.
Then you can choose one you want to use, assign suitable location and store it.

### Set OpenWeatherMap API key

The API key is long hash number which you shall
[get from OpenWeatherMap](https://home.openweathermap.org/users/sign_up). There are some personal API keys which are
for free however registration is required.


## Meteostation

Here we go ... once all above is passed, then simply press reset and wait till station is connected and forecast
displayed (it may take about one minute)

![Forecast](graphics/doc/forecast.png "Forecast")


## Reconfiguration

If you want to get into setup WEB page again, then you have restart meteostation and immediately hold **config**
button, till beep (it may take even half minute). Then QR codes appears on screen and configuration web server will be ready after next beep.


## Manual configuration

All items configured by WEB interface are at the end stored in [JSON](https://cs.wikipedia.org/wiki/JavaScript_Object_Notation) files
in root of internal file storage. If this files are missing, they are created automatically after first start of meteostation. This files
can be also edited manually, and are then used after restart. However be careful when editing them, especially files `connection.json`
and `location.json`, where `connection.json` which uses index to `location.json` as reference and is easy to break binding between
them.

Some of this files are described here:

### api.json

- `"units"` - Which units shall be used (`"metric"` or `"imperial"`).
- `"language"` - Which language shall be used  (`"cz"` or `"en"`).
- `"variant"` - How much days shall be displayed in forecast (number in range from 2 to 5, where 2 uses more detailed variant of forecast).
- `"apikey"` - `apikey` obtained from [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) used to download forecast.

### beep.json

- `"temp_balanced"` - Boolean telling if outdoor and indoor temperatures are balanced (so you can open window and start cooling your house).
- `"error_beep"` - Boolean telling if station shell you notify by beeping when some software error occur (goot for long time testing).

### spot.json

- `"ssid"` - Boolean telling if outdoor and indoor temperatures are balanced (so you can open window and start cooling your house).
- `"error_beep"` - Boolean telling if station shell you notify by beeping when some software error occur (goot for long time testing).


## Others

### Translations

Currently supported languages are English and Czech, however any support for translation to another language is welcommed.
If someone wants to add the new language, it can be done in folder [lang](https://github.com/ondiiik/meteoink/tree/master/simulator/lang).
Translation is always a dictionary where the key is english sentense and the value is its translation.

If some additional characters needs to be added, this shall be done in file [font2png.py](https://github.com/ondiiik/meteoink/blob/master/graphics/font2png.py).
There is a line just like following containing supported characters:

`chars = 'aábcčdďeéěfghiíjklmnňoópqrřsštťuúůvwxyýzžAÁBCČDĎEÉĚFGHIÍJKLMNOÓPQRŘSŠTŤUÚŮVWXYÝZŽ0123456789'~!@#$%^&*()_+-[]{};\:"|,./<>?°' + "'"`

You can add your missing characters here. Please add only characters which are used by meteostation as this will became to be part of bitmaps loaded
into meteostation during startup. More characters means longer startup and shorter battery life per one charging cycle.
