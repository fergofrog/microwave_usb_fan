#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from usbfan import Colour, ColourTheme, Column, Device, Message, Program, TextMessage, \
    MessageStyle, OpenTransition, CloseTransition

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

p = Program((TextMessage( "... HELLO WORLD! ...",
                theme = ColourTheme.Festive,
                message_style = MessageStyle.Anticlockwise,
                open_transition = OpenTransition.ToMiddle,
                close_transition = CloseTransition.DownUp),
             TextMessage( "Have a nice day :>",
                colour = Colour.yellow,
                message_style = MessageStyle.Flash ),
             TextMessage( "STAY COOOOOOL :>",
                theme = ColourTheme.Ice,
                open_transition = OpenTransition.DownUp,
                close_transition = CloseTransition.DownUp ),
             TextMessage( "MERRY CHRISTMAS",
                theme = ColourTheme.Christmas,
                message_style = MessageStyle.Clockwise,
                open_transition = OpenTransition.FromMiddle,
                close_transition = CloseTransition.ToMiddle) ))
             
# Open the device and program
d = Device()
d.program(p)
