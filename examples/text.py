#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from usbfan import Device, Program, TextMessage

# A program is made up of a list of Messages
# A "TextMessage" is a subclass of the generic Message class 
p = Program((TextMessage("Hello, World!"),
             TextMessage("How is everyone going?"),))
             
# Open the device and program
d = Device()
d.program(p)
