#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from usbfan import Colour, Column, Message, Device, Program, TextMessage

from PIL import Image, ImageDraw

if len(sys.argv) < 2:
    print("Give at least one image file as parameter")
    sys.exit(-1)

def map(c):
    MAP= {
        (False,False,False): None,
        (True,False,False): Colour.red,
        (False,True,False): Colour.green,
        (False,False,True): Colour.blue,
        (True,True,False): Colour.yellow,
        (True,False,True): Colour.magenta,
        (False,True,True): Colour.cyan,
        (True,True,True): Colour.white
    }

    cb = ( c[0] > 128, c[1] > 128, c[2] > 128 )
    return MAP[cb]

imgs = ()
for f in sys.argv[1:]:    
    im = Image.open(f)

    if im.width > Message.MAX_COLUMNS or im.height != Column.PIXELS:
        print("Image format mismatch.");
        break;

    img = [ ]

    # walk over all pixels
    for x in range(im.width):
        # check for most prominent color in this column
        l = { }
        c = [ ]
        for y in range(im.height):           
            p = map(im.getpixel((x,y)));
            if p:
                if p not in l: l[p] = 1
                else:          l[p] += 1
            c.append(p != None)
            
        img.append(Column(c, Colour.white if not l else max(l)))

    imgs = imgs + (Message(img), )
        
p = Program(imgs)
             
# Open the device and program
d = Device()
d.program(p)
