# Micro Wave USB Fan
This library is a pure Python reimplementation of the protocol used by various RGB USB fans based on the fan UF-211-06RGB that was designed by 刘保根 (Liu Baogen) and that is produced by 深圳市瑞声达电子有限公司 (Shenzhen Ruishengda Electronics Co.) as an OEM and also sold by themselves under the USTAR brand.  
Communication occurs using USB HID reports as a transport. This library uses
[hidapi](https://pypi.org/project/hidapi/) to do this across Linux, macOS,
FreeBSD and Windows.

## Installation
```sh
pip install microwave-usbfan
```

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

###  Mode Controls
For each message, you can define how it opens, what it does once displayed, and
what it does when closing.

```python
from usbfan import Colour, Column, Device, Message, Program, TextMessage, \
    MessageStyle, OpenTransition, CloseTransition

# We can cycle the rainbow here and fill all 144 columns
rainbow_colours = [Colour.red, Colour.yellow, Colour.green,
                   Colour.cyan, Colour.blue, Colour.magenta]
rainbow = [Column([True] * 11,
                  rainbow_colours[i % len(rainbow_colours)])
           for i in range(Message.MAX_COLUMNS)]
p = Program((
    TextMessage("Here comes the rainbow!",
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
```

# UF-211-06RGB details
Official Alibaba shop entries: [1](https://www.alibaba.com/product-detail/Factory-Direct-Flexible-USB-Fan-Programmable_1600428130893.html),[2](https://www.alibaba.com/product-detail/Flexible-USB-Message-Fan-RGB-Multicolor_1600428182360.html),[3](https://www.alibaba.com/product-detail/Flexible-USB-Programmable-Message-Fan-Software_60530542736.html),[4](https://www.alibaba.com/product-detail/Patented-USB-Flexible-Program-Led-Message_60488878681.html),[5](https://www.alibaba.com/product-detail/2016-Hot-fashion-best-gifts-dc_60495560842.html),[6](https://www.alibaba.com/product-detail/USB-Programmable-Message-Fan-LED-Messaege_60749056487.html)  
Power: USB  
Color: Silver  
Size: 40 x 0.7 cm; 8.8 cm fan diameter  
Fan Material: PVC blade & metal neck  
Certificates: CE/ROHS/EMC/FCC  

[More info](https://github.com/Ventto/pearlfan/issues/11#issuecomment-2508454088)

# Known rebrands 

Jaycar GJ1031  
Saytay USB LED Fan Message Fan 
