if [ "$1" ]
then
    PORT="$1"
else
    PORT="/dev/ttyUSB0"
fi

if [ "$2" ]
then
    FW="$2"
else
    FW="meteoink.bin"
fi

esptool.py --port $PORT erase_flash

esptool.py \
    --chip esp32 \
    -p $PORT \
    -b 460800 \
    --before=default_reset \
    --after=hard_reset \
    write_flash \
    --flash_mode dio \
    --flash_freq 40m \
    --flash_size 4MB \
    0x1000 \
    meteoink.bin
