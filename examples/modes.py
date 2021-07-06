#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from usbfan import Colour, Column, Device, Message, Program, TextMessage, \
    MessageStyle, OpenTransition, CloseTransition

print("MAX_COLUMNS:", Message.MAX_COLUMNS, "x", Column.PIXELS);

# -> 144 * 11 pixel
# Column.PIXELS

# We can cycle the rainbow here and fill all 144 columns
rainbow_colours = [Colour.red, Colour.yellow, Colour.green,
                   Colour.cyan, Colour.blue, Colour.magenta]
rainbow = [Column([True] * 11,
                  rainbow_colours[i % len(rainbow_colours)])
           for i in range(Message.MAX_COLUMNS)]
p = Program((
    TextMessage("Hallo Maya & Fabian ...",
                message_style=MessageStyle.Flash,
                open_transition=OpenTransition.DownUp,
                close_transition=CloseTransition.DownUp),
    Message(rainbow,
            message_style=MessageStyle.Clockwise,
            open_transition=OpenTransition.FromMiddle,
            close_transition=CloseTransition.ToMiddle),
))

# Open the device and program
d = Device()
d.program(p)
