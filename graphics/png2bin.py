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


BLACK       = 0
WHITE       = 15
TRANSPARENT = 1

pg          = '0 23456789ABCDEF'


def rgb2color(rgba):
    if (rgba[3] < 128):
        return TRANSPARENT
    
    c   = (rgba[0] + rgba[1]) // 2
    
    if rgba[2] in range(c - 3, c + 3):
        c = (rgba[0] + rgba[1] + rgba[2]) // 3
    
    c  *= WHITE
    c //= 127
    
    if c == TRANSPARENT:
        c += 1
    
    return c


def convert(src_file_name, dst_file_name, scale = 1):
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
            bits_count += 4
            bit_mask    = bit_mask << 4
            color       = rgb2color(rgba)
            pix         = color & WHITE
            bit_mask    = bit_mask | pix
                
            print(pg[pix], end = '')
            
            if 8 == bits_count:
                bit_mask = ((bit_mask >> 4) | (bit_mask << 4)) & 0xFF
                dst.write(struct.pack('=B', bit_mask))
                
                print('|', end = '')
                bits_count = 0
                bit_mask   = 0
                
        if not 0 == bits_count:
            bit_mask  = bit_mask << 4
            bit_mask |= TRANSPARENT
            
            bit_mask = ((bit_mask >> 4) | (bit_mask << 4)) & 0xFF
            dst.write(struct.pack('=B', bit_mask))
            
            print('~' + '|', end = '')
            cnt += (bits_count % 2)
        print('')
    print('')
        
    dst.close()


src_dir = 'bitmap/png'
dst_fmt = '../micropython/bitmap/%i/%s.bim'

for src_name in os.listdir(src_dir):
    src = os.path.join(src_dir,src_name)
    
    for scale in (1,2,3,4,5):
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
