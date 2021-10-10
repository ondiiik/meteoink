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


def convert(name, src_file_name, dst, scales = (None,), mask = (Color.BLACK, Color.WHITE, Color.YELLOW, Color.NON_YELLOW)):
    import imageio
    import os
    
    use_scale = not scales[0] is None
    
    if use_scale:
        dst.write(f'    {repr(name)} : {{\n')
    else:
        dst.write(f'    {repr(name)} : \n')
    
    for scale in scales:
        if scale is None:
            scale = 1
        
        png    = imageio.imread(src_file_name)
        width  = int(png.shape[1]) // scale
        height = int(png.shape[0]) // scale
        
        if use_scale:
            dst.write(f'        {scale} : ({width}, {height},\n')
        else:
            dst.write(f'        ({width}, {height},\n')
        
        buff = bytearray()
        
        print(f'Converting "{src_file_name}" to "{name}" - {width} x {height} ({scale} : 1) ...')
        # Prepare all 3 layers
        for mask_color in mask:
            scale_y = 0
            cnt     = 0
            
            for row in png:
                scale_y += 1
                
                if scale_y < scale:
                    continue
                
                #print('|', end = '')
                
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
                        
                    #print('0' if pix == 1 else ' ', end = '')
                    
                    if 8 == bits_count:
                        if (mask_color == Color.BLACK) or (mask_color == Color.YELLOW):
                            bit_mask = (~bit_mask & 0xFF)
                            
                        buff.extend(bytearray([bit_mask]))
                        
                        #print('|', end = '')
                        bits_count = 0
                        bit_mask   = 0
                        
                if not 0 == bits_count:
                    bit_mask = bit_mask << (8 - bits_count)
                    
                    if (mask_color == Color.BLACK) or (mask_color == Color.YELLOW):
                        bit_mask = (~bit_mask & 0xFF)
                        
                    buff.extend(bytearray([bit_mask]))
                    
                    #print('~' * (8 - bits_count) + '|', end = '')
                    cnt += (bits_count % 2)
                #print('')
            #print('')
        
        if use_scale:
            dst.write(f' memoryview({bytes(buff)})),\n')
        else:
            dst.write(f' memoryview({bytes(buff)}))\n')
    
    if use_scale:
        dst.write('    },\n\n')
    else:
        dst.write('     ,\n\n')


src_dir = os.path.abspath('bitmap/png')
dst_dir = os.path.abspath('../micropython/bitmap')

    
try:
    os.mkdir(dst_dir)
except FileExistsError:
    pass

with open(os.path.join(dst_dir, 'bmp.py'), 'w') as dst:
    dst.write('bmp = {\n')
    
    for src_name in os.listdir(src_dir):
        src = os.path.join(src_dir, src_name)
        convert(src_name[:-4], src, dst, (1, 4, 5))
    
    dst.write('}\n')


src_dir = os.path.abspath('bitmap/font')
fsize   = 0

with open(os.path.join(dst_dir, 'fonts.py'), 'w') as dst:
    dst.write('fonts = {\n')
    
    for src_name in sorted(os.listdir(src_dir), key = lambda n: int(n[:2], 16) * 256 + int(n[2:-4], 16)):
        fs   = int(src_name[:2], 16)
        
        if fsize != fs:
            if 0 != fsize:
                dst.write('},\n')
            dst.write(f'  {fs} : {{\n')
            fsize = fs
            
        
        src  = os.path.join(src_dir, src_name)
        ch   = int(src_name[2:-4], 16)
        
        convert(ch, src, dst)
    
    dst.write('},\n}\n')

