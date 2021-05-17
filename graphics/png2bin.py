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


class Color:
    BLACK        = 1
    WHITE        = 2
    YELLOW       = 3
    NON_YELLOW   = 4
    TRANSPARENT  = 5


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


def convert(src_file_name, dst_file_name, scale = 1, mask = (Color.BLACK, Color.WHITE, Color.YELLOW, Color.NON_YELLOW)):
    import imageio
    import struct
    import os
    
    try:
        os.mkdir(os.path.dirname(dst_file_name))
    except FileExistsError:
        pass
    
    png    = imageio.imread(src_file_name)
    dst    = open(dst_file_name, 'wb')
    width  = int(png.shape[1]) // scale
    height = int(png.shape[0]) // scale
    
    print("Converting '%s' to '%s' - %i x %i (%i : 1) ..." % (src_file_name, dst_file_name, width, height, scale))
    
    dst.write(struct.pack('<HH', width, height))
    
    
    # Prepare all 3 layers
    for mask_color in mask:
        scale_y = 0
        cnt     = 0
        
        for row in png:
            scale_y += 1
            
            if scale_y < scale:
                continue
            
            print('|', end = '')
            
            scale_y    = 0
            cnt       += 1
            bit_mask   = 0
            bits_count = 0
            scale_x    = 0
            
            for rgba in row:
                scale_x += 1
                
                if scale_x < scale:
                    continue
                
                scale_x     = 0
                cnt        += 1
                bits_count += 1
                bit_mask    = bit_mask << 1
                color       = rgb2color(rgba)
                pix         = 1 if mask_color == color[cnt % 2] else 0
                
                if mask_color == Color.NON_YELLOW:
                    pix = 0 if (Color.YELLOW == color[cnt % 2]) or (Color.TRANSPARENT == color[cnt % 2]) else 1
                    
                bit_mask = bit_mask | pix
                    
                print('0' if pix == 1 else ' ', end = '')
                
                if 8 == bits_count:
                    if (mask_color == Color.BLACK) or (mask_color == Color.YELLOW):
                        bit_mask = (~bit_mask & 0xFF)
                        
                    dst.write(struct.pack('=B', bit_mask))
                    
                    print('|', end = '')
                    bits_count = 0
                    bit_mask   = 0
                    
            if not 0 == bits_count:
                bit_mask = bit_mask << (8 - bits_count)
                
                if (mask_color == Color.BLACK) or (mask_color == Color.YELLOW):
                    bit_mask = (~bit_mask & 0xFF)
                    
                dst.write(struct.pack('=B', bit_mask))
                
                print('~' * (8 - bits_count) + '|', end = '')
                cnt += (bits_count % 2)
            print('')
        print('')
        
    dst.close()


src_dir = 'bitmap/png'
dst_fmt = '../micropython/bitmap/%i/%s.bim'

for src_name in os.listdir(src_dir):
    src = os.path.join(src_dir,src_name)
    
    for scale in (1,4,5):
        dst = dst_fmt % (scale, src_name[:-4])
        convert(src, dst, scale)

font_dir = '../micropython/bitmap/f'
    
try:
    os.mkdir(font_dir)
except FileExistsError:
    pass

src_dir = 'bitmap/font'
dst_fmt = font_dir + '/%i/%i.bim'

for src_name in os.listdir(src_dir):
    src  =  os.path.join(src_dir,src_name)
    size =  int(src_name[0:2],  16)
    ch   =  int(src_name[2:-4], 16)
    dst  =  dst_fmt % (size, ch)
    convert(src, dst)
