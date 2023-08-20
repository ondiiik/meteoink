#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Needs freetype-py>=1.0

# For more info see:
# http://dbader.org/blog/monochrome-font-rendering-with-freetype-and-python

# The MIT License (MIT)
#
# Copyright (c) 2013 Daniel Bader (http://dbader.org)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys
import os
import imageio
import numpy as np
from itertools import product
from ctypes import c_uint8, LittleEndianStructure, Union
from pathlib import Path
from pprint import pprint


class Flags_bits(LittleEndianStructure):
    _fields_ = (("c1", c_uint8, 4), ("c0", c_uint8, 4))


class Flags(Union):
    _fields_ = [("colors", Flags_bits), ("asbyte", c_uint8)]


class Color:
    BLACK = 0
    WHITE = 15
    GRAY = 13
    TRANSPARENT = 1


from itertools import combinations

usable_colors = (
    Color.BLACK,
    Color.WHITE,
    Color.GRAY,
)

usable_colors_map = {
    Color.BLACK: np.array((0, 0, 0)),
    Color.WHITE: np.array((255, 255, 255)),
    Color.GRAY: np.array((128, 128, 128)),
}


def rgb2color(rgba):
    try:
        if rgba[3] < 128:
            return Color.TRANSPARENT
    except:
        ...  # No transparency

    rgba = np.array(rgba[:3])
    mag_max = 1024
    detected = Color.TRANSPARENT

    for color, rgb in usable_colors_map.items():
        vect = rgba - rgb
        mag = np.linalg.norm(vect)
        if mag < mag_max:
            mag_max = mag
            detected = color
            if mag < 1:
                break

    return detected


def convert_bitmap(name, src, bmp, scales):
    bmp[name] = dict()
    icon = bmp[name]

    for scale in scales:
        png = imageio.imread(src)
        width = int(png.shape[1]) // scale
        height = int(png.shape[0]) // scale
        bwidth = width + (1 if width % 2 else 0)

        buff = bytearray()

        print(f'Converting "{src}" to "{name}" - {bwidth} x {height} ({scale} : 1) ...')
        pix = Flags()
        pix.asbyte = 0

        im = np.zeros((bwidth, height), dtype=np.uint8)

        for y, row in zip(range(height), png[scale // 2 :: scale]):
            for x, rgba in zip(range(width), row[scale // 2 :: scale]):
                color = rgb2color(rgba)
                im[x][y] = color

        for y in range(height):
            for x in range(width):
                color = im[x][y]
                if x % 2:
                    pix.colors.c1 = color
                    buff.extend([pix.asbyte])
                else:
                    pix.colors.c0 = color
            if not x % 2:
                pix.colors.c1 = Color.TRANSPARENT
                buff.extend([pix.asbyte])

        icon[scale] = bwidth, height, buff
        if "greetings" in str(src):
            break


def convert_char(name, src, fv):
    png = imageio.imread(src)
    width = int(png.shape[1])
    height = int(png.shape[0])
    bwidth = width + (1 if width % 2 else 0)

    print(f'Converting "{src}" (ord {name}) - {bwidth} x {height} ...')
    pix = Flags()
    pix.asbyte = 0

    im = np.zeros((bwidth, height), dtype=np.uint8)

    for y, row in zip(range(height), png):
        for x, rgba in zip(range(width), row):
            color = rgb2color(rgba)
            im[x][y] = color

    buff = bytearray()
    for y in range(height):
        for x in range(width):
            color = im[x][y]
            if x % 2:
                pix.colors.c1 = color
                buff.extend([pix.asbyte])
            else:
                pix.colors.c0 = color
        if not x % 2:
            pix.colors.c1 = Color.TRANSPARENT
            buff.extend([pix.asbyte])

    fv[name] = bwidth, height, buff


src_dir = Path("bitmap/png/gs").resolve()
wind_dir = Path("bitmap/wind/gs").resolve()
dst_bin_dir = Path("../micropython/bitmaps/gs").resolve()
dst_py_dir = Path("../micropython/bitmap/gs").resolve()
wind_dir.mkdir(exist_ok=True)
dst_bin_dir.mkdir(exist_ok=True)


# =========================================================================================
# Create bitmaps
# =========================================================================================
bitmap_py = dst_py_dir.joinpath("bmp.py")
bitmap_bin = dst_bin_dir.joinpath("bmp.bin")

with bitmap_py.open("w") as py, bitmap_bin.open("wb") as bin:
    py.write(
        """from ulogging import getLogger
logger = getLogger(__name__)

BMP = """
    )

    #   # Build basic structure
    bmp = {}
    srcs = os.listdir(src_dir)
    srcs.sort()
    for src_name in srcs:
        if not src_name.endswith(".png"):
            continue
        src = src_dir.joinpath(src_name)
        convert_bitmap(src_name[:-4], src, bmp, (1, 2, 3))

    # Move binary data to binary file
    idx = 0
    for size in bmp.values():
        for variant, value in size.items():
            data = value[2]
            bin.write(data)
            size[variant] = [value[0], value[1], idx, "bmp"]
            idx += len(data)

    pprint(bmp, py, width=160)


# =========================================================================================
# Create fonts
# =========================================================================================
src_dir = Path("bitmap/font/gs")
fonts_py = dst_py_dir.joinpath("fonts.py")
fonts_bin = dst_bin_dir.joinpath("fonts.bin")

with fonts_py.open("w") as py, fonts_bin.open("wb") as bin:
    py.write(
        """from ulogging import getLogger
logger = getLogger(__name__)

FONTS = """
    )

    #   # Build basic structure
    dirs = os.listdir(src_dir)
    dirs.sort(
        key=lambda n: int(n[:1], 16) * 0x1000
        + int(n[1:3], 16) * 0x100000
        + int(n[3:-4], 16)
    )
    fonts = {}

    for src_name in dirs:
        fs = int(src_name[1:3], 16)
        fs = fonts.setdefault(fs, dict())
        fv = int(src_name[:1], 16)
        fv = fs.setdefault(fv, {fv: dict()})[fv]
        ch = int(src_name[3:-4], 16)
        src = os.path.join(src_dir, src_name)
        convert_char(ch, src, fv)

    # Move binary data to binary file
    idx = 0
    reduced = [ord(c) for c in "0123456789.°C%RH"]
    for size, values in fonts.items():
        for q in values.values():
            for w in values.values():
                for font in w.values():
                    for variant, value in list(font.items()):
                        data = value[2]
                        if isinstance(data, int):
                            continue
                        if (size < 50) or (variant in reduced):
                            bin.write(data)
                            font[variant] = [value[0], value[1], idx, "fonts"]
                            idx += len(data)
                        else:
                            font.pop(variant)

    pprint(fonts, py, width=160)
