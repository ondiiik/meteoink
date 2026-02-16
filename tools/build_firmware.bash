#!/usr/bin/env bash
set -Exeuo pipefail


# Prepare build directory
CWD=$PWD
BUILD_ROOT="$PWD"
if [ "$(basename $BUILD_ROOT)" != ".out" ]
then
    BUILD_ROOT="$BUILD_ROOT/.out"
    mkdir -p "$BUILD_ROOT"
    cd "$BUILD_ROOT"
fi

if [ ${0:0:1} != "." ] && [ ${0:0:1} != "/" ]
then
    SRC_ROOT="$(dirname $(dirname $(realpath $CWD/$0)))"
else
    SRC_ROOT="$(dirname $(dirname $(realpath $0)))"
fi


# Download MicroPyhon sources
if [ ! -d "$BUILD_ROOT/micropython" ]
then
    git clone https://github.com/micropython/micropython.git --recursive -b v1.27.0
fi

# Install esp-idf
if [ ! -d "$BUILD_ROOT/esp-idf" ]
then
    git clone -b v5.5.1 --recursive https://github.com/espressif/esp-idf.git
fi

if [ ! -d "$HOME/.espressif/python_env/idf5.5_py3.12_env" ]
then
    cd "$BUILD_ROOT/esp-idf"
    ./install.sh esp32
    cd "$BUILD_ROOT"
fi

. $BUILD_ROOT/esp-idf/export.sh


# Patch micropython sources
rsync -av "/home/ondiiik/Development/micropython/meteo/meteo_py/tools/mpy_patch/" "$BUILD_ROOT/micropython"
sed 's~$(METEOINK_SRC_ROOT)~'"$SRC_ROOT/micropython"'~g' < "$SRC_ROOT/tools/manifest.py" > "$BUILD_ROOT/micropython/ports/esp32/boards/ESP32_GENERIC/manifest.py"


# Build MicroPython firmware
rm -rf "$BUILD_ROOT/micropython/ports/esp32/build-ESP32_GENERIC-SPIRAM"
rm -f "$BUILD_ROOT/vindriktning-mpy.bin"
cd "$BUILD_ROOT/micropython"
make -C mpy-cross
cd "$BUILD_ROOT/micropython/ports/esp32"
BOARD_VARIANT=SPIRAM make -j$(nproc) submodules
BOARD_VARIANT=SPIRAM make -j$(nproc) all
cp "$BUILD_ROOT/micropython/ports/esp32/build-ESP32_GENERIC-SPIRAM/firmware.bin" "$BUILD_ROOT/meteoink.bin"
