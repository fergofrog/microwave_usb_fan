#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from usbfan import Colour, ColourTheme, Column, Device, Message, Program, TextMessage, \
    MessageStyle, OpenTransition, CloseTransition

from PIL import Image, ImageDraw

# A program is made up of a list of Messages
# A "TextMessage" is a subclass of the generic Message class 

# "colour" can be one of:
# Colour.red
# Colour.yellow
# Colour.green
# Colour.cyan
# Colour.blue
# Colour.magenta
# Colour.white

# "theme" can be one of:
# ColourTheme.Ice
# ColourTheme.Fire
# ColourTheme.Festive
# ColourTheme.Christmas
# ColourTheme.Rainbow

# Colour map for any loaded images
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

# Load some images
imgs = ()
for f in ( "stars-hello.png", "hyperspace.png", "lightsabers.png", "snake.png" ):    
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

# chr(1) = Diamond
# chr(147) = Candy cane

# Here's where we define the Program (set of pictures) that the fan runs
# A Program can have up to six pictures (Text Messages or Images)

p = Program(( imgs[0],
              TextMessage( chr(1) + " Greetings to all! " + chr(1),
                theme = ColourTheme.Festive,
                message_style = MessageStyle.Anticlockwise,
                open_transition = OpenTransition.ToMiddle,
                close_transition = CloseTransition.DownUp),
             imgs[2],
             TextMessage( "(= Have a nice day =)",
                colour = Colour.yellow,
                message_style = MessageStyle.Flash ),
             TextMessage( "Stay coooOOOOooool :)",
                theme = ColourTheme.Ice,
                open_transition = OpenTransition.DownUp,
                close_transition = CloseTransition.DownUp ),
             #TextMessage( "... or HOT!!! ",
             #   theme = ColourTheme.Fire,
             #   open_transition = OpenTransition.DownUp,
             #   close_transition = CloseTransition.DownUp ),
             #TextMessage( "Paint The Whole World...",
             #   theme = ColourTheme.Rainbow,
             #   open_transition = OpenTransition.DownUp,
             #   close_transition = CloseTransition.DownUp ),
             TextMessage( chr(147) + chr(147) + " Merry Christmas " + chr(147) + chr(147),
                theme = ColourTheme.Christmas,
                message_style = MessageStyle.Clockwise,
                open_transition = OpenTransition.FromMiddle,
                close_transition = CloseTransition.ToMiddle)
             #imgs[1] 
))
             
# Open the device and program
d = Device()
d.program(p)
