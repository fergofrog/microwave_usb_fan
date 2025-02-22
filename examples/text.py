#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from usbfan import Device, Program, TextMessage, Colour

# A program is made up of a list of Messages
# A "TextMessage" is a subclass of the generic Message class

r = Colour.red
y = Colour.yellow
g = Colour.green
c = Colour.cyan
b = Colour.blue
m = Colour.magenta

letters = [x for x in "Hello World "]
colors =  [r, y, g, c, b, b, r, y, g, c, b, b]

message0 = TextMessage(
    letters + letters, colors + colors
)
print(message0.visualize())

p = Program(
    (
        message0,
        TextMessage("How is everyone going?", Colour.green),
    )
)

# Open the device and program
d = Device()
d.program(p)
