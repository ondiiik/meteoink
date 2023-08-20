if [ "$1" ]
then
    PORT="$1"
else
    PORT="/dev/ttyUSB0"
fi

esptool.py \
    --port /dev/ttyUSB0 \
    erase_flash

esptool.py \
    --chip esp32 \
    -p /dev/ttyUSB0 \
    -b 460800 \
    --before=default_reset \
    --after=hard_reset \
    write_flash \
    --flash_mode dio \
    --flash_freq 40m \
    --flash_size 4MB \
    0x1000 bootloader.bin \
    0x10000 micropython.bin \
    0x8000 partition-table.bin

#esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 micropython.bin
