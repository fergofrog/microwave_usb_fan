#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from usbfan import Colour, Column, Device, Message, Program

# A generic "Message" is made up of 1 to 144 "Column" object
# A "Column" has 11 boolean pixels and a "Colour"
columns = [Column([True] + [False] * 10, Colour.red)]
for _ in range(7):
    columns.append(Column([False] * 11, Colour.red))
p = Program((Message(columns),))

# Open the device and program
d = Device()
d.program(p)
