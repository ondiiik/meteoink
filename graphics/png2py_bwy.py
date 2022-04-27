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
import numpy
from itertools import product
from ctypes import c_uint8, LittleEndianStructure, Union
from pathlib import Path


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


def rgb2color(rgba):
    if (rgba[3] < 128):
        return (Color.TRANSPARENT, Color.TRANSPARENT)

    if (rgba[0] != rgba[2]):
        if rgba[2] > 127:
            return (Color.YELLOW, Color.WHITE)
        if rgba[0] < 85:
            return (Color.YELLOW, Color.BLACK)
        return (Color.YELLOW, Color.YELLOW)

    if rgba[0] > 170:
        return (Color.WHITE, Color.WHITE)
    if rgba[0] < 85:
        return (Color.BLACK, Color.BLACK)
    return (Color.WHITE, Color.BLACK)


def convert(name, src_file_name, dst, scales=(None,)):
    use_scale = not scales[0] is None

    if use_scale:
        dst.write(f'        {repr(name)} : {{')
    else:
        dst.write(f'    {repr(name)} : {{ 0 : ')

    for scale in scales:
        if scale is None:
            scale = 1

        png = imageio.imread(src_file_name)
        width = int(png.shape[1]) // scale
        height = int(png.shape[0]) // scale
        bwidth = width + (1 if width % 2 else 0)

        if use_scale:
            dst.write(f'{scale} : ({bwidth}, {height}, ')
        else:
            dst.write(f'({bwidth}, {height}, ')

        buff = bytearray()

        print(f'Converting "{src_file_name}" to "{name}" - {bwidth} x {height} ({scale} : 1) ...')
        pix = Flags()
        pix.asbyte = 0

        im = numpy.zeros((bwidth, height), dtype=numpy.uint8)

        for y, row in zip(range(height), png[scale // 2::scale]):
            for x, rgba in zip(range(width), row[scale // 2::scale]):
                color = rgb2color(rgba)[(x + y) % 2]
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

        dst.write(f' bytearray({bytes(buff)})),')
        if use_scale:
            dst.write('\n')
    dst.write('    },\n')


src_dir = Path('bitmap/png/bwy').resolve()
dst_dir = Path('../micropython/bitmap/bwy').resolve()
dst_dir.mkdir(exist_ok=True)

bitmap = dst_dir.joinpath('bmp.py')
bitmap_tmp = dst_dir.joinpath('bmp.py_')

with bitmap_tmp.open('w') as dst:
    dst.write('''from ulogging import getLogger
logger = getLogger(__name__)

bmp = {''')

    for src_name in os.listdir(src_dir):
        src = os.path.join(src_dir, src_name)
        convert(src_name[:-4], src, dst, (1, 4, 5))

    dst.write('}\n')

print(f'Running autopep on {str(bitmap)}')
os.system(f'autopep8 "{str(bitmap_tmp)}" > {str(bitmap)}')
os.system(f'rm -f {str(bitmap_tmp)}')


src_dir = Path('bitmap/font/bwy')
fsize = 0

fonts_path = dst_dir.joinpath('fonts.py')
fonts_path_tmp = dst_dir.joinpath('fonts.py_')

with fonts_path_tmp.open('w') as dst:
    dst.write('''from ulogging import getLogger
logger = getLogger(__name__)

fonts = {''')

    for src_name in sorted(os.listdir(src_dir), key=lambda n: int(n[:2], 16) * 256 + int(n[2:-4], 16)):
        fs = int(src_name[:2], 16)

        if fsize != fs:
            if 0 != fsize:
                dst.write('},\n')
            dst.write(f'    {fs} : {{')
            fsize = fs

        src = os.path.join(src_dir, src_name)
        ch = int(src_name[2:-4], 16)

        convert(ch, src, dst)

    dst.write('},\n}\n')

print(f'Running autopep on {str(fonts_path)}')
os.system(f'autopep8 "{str(fonts_path_tmp)}" > {str(fonts_path)}')
os.system(f'rm -f {str(fonts_path_tmp)}')
