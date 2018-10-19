# Micro Wave USB Fan
This library is a pure Python reimplementation of the Jaycar RGB USB LED fan
([GH1031](https://www.jaycar.com.au/programmable-usb-fan/p/GH1031)) protocol.
Communication occurs using USB HID reports as a transport. This library uses
[hidapi](https://pypi.org/project/hidapi/) to do this across Linux, macOS,
FreeBSD and Windows.

## Example Implementation
### Two Text Messages
```python
from usbfan import Device, Program, TextMessage

# A program is made up of a list of Messages
# A "TextMessage" is a subclass of the generic Message class 
p = Program((TextMessage("Hello, World!"),
             TextMessage("How is everyone going?"),))
             
# Open the device and program
d = Device()
d.program(p)
```

### Single Red Dot
```python
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
```

### Rainbow Message
```python
from usbfan import Colour, Column, Device, Message, Program, TextMessage

# We can cycle the rainbow here and fill all 144 columns
rainbow_colours = [Colour.red, Colour.yellow, Colour.green,
                   Colour.cyan, Colour.blue, Colour.magenta]
rainbow = [Column([True] * 11,
                  rainbow_colours[i % len(rainbow_colours)])
           for i in range(Message.MAX_COLUMNS)]
p = Program((
    TextMessage("Here comes the rainbow!"),
    Message(rainbow),
))

# Open the device and program
d = Device()
d.program(p)
```