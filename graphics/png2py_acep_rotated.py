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
    _fields_ = (("c1", c_uint8, 4),
                ("c0", c_uint8, 4))


class Flags(Union):
    _fields_ = [("colors", Flags_bits),
                ("asbyte", c_uint8)]


class Color:
    BLACK = 0
    WHITE = 1
    GREEN = 2
    BLUE = 3
    RED = 4
    YELLOW = 5
    ORANGE = 6
    TRANSPARENT = 7


from itertools import combinations
usable_colors = Color.BLACK, Color.WHITE, Color.GREEN, Color.BLUE, Color.RED, Color.YELLOW, Color.ORANGE
color_combinations = [(c, c) for c in usable_colors]
color_combinations += (Color.WHITE, Color.BLACK), (Color.WHITE, Color.BLUE), (Color.WHITE, Color.YELLOW), (Color.GREEN, Color.BLUE), (Color.RED, Color.BLUE)
color_combinations += list(combinations(usable_colors, 2))

usable_colors_map = {Color.BLACK: np.array((0, 0, 0)),
                     Color.WHITE: np.array((255, 255, 255)),
                     Color.GREEN: np.array((0, 255, 0)),
                     Color.BLUE: np.array((0, 0, 255)),
                     Color.RED: np.array((255, 0, 0)),
                     Color.YELLOW: np.array((255, 255, 0)),
                     Color.ORANGE: np.array((255, 127, 0))}

colr_sets = {(c1, c2): ((usable_colors_map[c1] + usable_colors_map[c2]) / 2).astype(np.uint8) for c1, c2 in color_combinations}


def rgb2color(rgba):
    try:
        if (rgba[3] < 128):
            return Color.TRANSPARENT, Color.TRANSPARENT
    except:
        pass  # No transparency

    rgba = np.array(rgba[:3])
    mag_max = 1024
    detected = Color.TRANSPARENT, Color.TRANSPARENT

    for colors, rgb in colr_sets.items():
        vect = rgba - rgb
        mag = np.linalg.norm(vect)
        if mag < mag_max:
            mag_max = mag
            detected = colors
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
        bheight = height + (1 if height % 2 else 0)

        buff = bytearray()

        print(f'Converting "{src}" to "{name}" - {width} x {bheight} ({scale} : 1) ...')
        pix = Flags()
        pix.asbyte = 0

        im = np.zeros((bheight, width), dtype=np.uint8)

        for y, row in zip(range(height), png[scale // 2::scale]):
            for x, rgba in zip(range(width), row[scale // 2::scale]):
                color = rgb2color(rgba)[(x + y) % 2]
                im[y][x] = color

        for x in range(width):
            for y in range(height):
                color = im[y][width - x - 1]
                if y % 2:
                    pix.colors.c1 = color
                    buff.extend([pix.asbyte])
                else:
                    pix.colors.c0 = color
            if not y % 2:
                pix.colors.c1 = Color.TRANSPARENT
                buff.extend([pix.asbyte])

        icon[scale] = bheight, width, buff


def convert_char(name, src, fv):
    png = imageio.imread(src)
    width = int(png.shape[1])
    height = int(png.shape[0])
    bheight = height + (1 if height % 2 else 0)

    print(f'Converting "{src}" (ord {name}) - {width} x {bheight} ...')
    pix = Flags()
    pix.asbyte = 0

    im = np.zeros((bheight, width), dtype=np.uint8)

    for y, row in zip(range(height), png):
        for x, rgba in zip(range(width), row):
            color = rgb2color(rgba)[(x + y) % 2]
            im[y][x] = color

    buff = bytearray()
    for x in range(width):
        for y in range(height):
            color = im[y][width - x - 1]
            if y % 2:
                pix.colors.c1 = color
                buff.extend([pix.asbyte])
            else:
                pix.colors.c0 = color
        if not y % 2:
            pix.colors.c1 = Color.TRANSPARENT
            buff.extend([pix.asbyte])

    fv[name] = bheight, width, buff


# =========================================================================================
# Build wind icons
# =========================================================================================
src_dir = Path('bitmap/png/acep').resolve()
wind_dir = Path('bitmap/wind/acep').resolve()
wind_dir.mkdir(exist_ok=True)

for level in range(5):
    print(f'Wind icons level {level}')
    src = src_dir.joinpath(f'svg/wa{level}.png')

    for angle in range(0, 360, 15):
        dst = wind_dir.joinpath(f'wa{level}{angle}.png')
        os.system(f'convert "{src}" -background none -rotate {angle} "{dst}"')

dst_dir = Path('../micropython/bitmap/acep_rotated').resolve()
dst_dir.mkdir(exist_ok=True)
wind = dst_dir.joinpath('wind.py')

with wind.open('w') as dst:
    dst.write('''from ulogging import getLogger
logger = getLogger(__name__)

WIND = ''')

    wind = {}
    srcs = os.listdir(wind_dir)
    srcs.sort()
    for src_name in srcs:
        if not src_name.endswith('.png'):
            continue
        level = int(src_name[2:3])
        level = wind.setdefault(level, dict())
        angle = int(src_name[3:-4])
        # angle = level.setdefault(angle, dict())
        src = wind_dir.joinpath(src_name)
        convert_bitmap(angle, src, level, (1, 4))

    pprint(wind, dst, width=160)


# =========================================================================================
# Create bitmaps
# =========================================================================================
bitmap = dst_dir.joinpath('bmp.py')

with bitmap.open('w') as dst:
    dst.write('''from ulogging import getLogger
logger = getLogger(__name__)

BMP = ''')

    bmp = {}
    srcs = os.listdir(src_dir)
    srcs.sort()
    for src_name in srcs:
        if not src_name.endswith('.png'):
            continue
        src = src_dir.joinpath(src_name)
        convert_bitmap(src_name[:-4], src, bmp, (1, 4, 5))

    pprint(bmp, dst, width=160)


# =========================================================================================
# Create fonts
# =========================================================================================
src_dir = Path('bitmap/font/acep')
fonts_path = dst_dir.joinpath('fonts.py')

with fonts_path.open('w') as dst:
    dst.write('''from ulogging import getLogger
logger = getLogger(__name__)

FONTS = ''')

    dirs = os.listdir(src_dir)
    dirs.sort(key=lambda n: int(n[:1], 16) * 0x1000 + int(n[1:3], 16) * 0x100000 + int(n[3:-4], 16))
    fonts = {}

    for src_name in dirs:
        fs = int(src_name[1:3], 16)
        fs = fonts.setdefault(fs, dict())
        fv = int(src_name[:1], 16)
        fv = fs.setdefault(fv, {fv: dict()})[fv]
        ch = int(src_name[3:-4], 16)
        src = os.path.join(src_dir, src_name)
        convert_char(ch, src, fv)

    pprint(fonts, dst, width=160)
