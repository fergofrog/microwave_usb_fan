from enum import IntEnum
from math import floor, log2
from typing import Iterator, Optional, Sequence, Union


class Colour(IntEnum):
    # primary
    red = 0b00100000_00000000
    blue = 0b01000000_00000000
    green = 0b10000000_00000000

    # mixes
    magenta = 0b01100000_00000000
    yellow = 0b10100000_00000000
    cyan = 0b11000000_00000000

    # everything
    white = 0b11100000_00000000


class Column:
    PIXELS = 11

    def __init__(self, pixels: Optional[Sequence[bool]]=None,
                 colour: Union[int, Colour]=Colour.red):
        if pixels:
            try:
                if not all(isinstance(p, bool) for p in pixels):
                    raise ValueError("pixels must be an iterable of bool's")
                elif len(pixels) != Column.PIXELS:
                    raise ValueError(f"pixels must be an iterable of "
                                     f"{Column.PIXELS} bool's")
            except TypeError:
                raise ValueError("pixels must be an iterable of bool's")
            self.pixels = list(pixels)
        else:
            self.pixels = [False] * Column.PIXELS

        if not isinstance(colour, (int, Colour)):
            raise ValueError('colour must be an int or Colour')
        if colour & Colour.white != colour:
            raise ValueError('bad colour value')
        self.colour = colour

    def __bytes__(self) -> bytes:
        b = 0x0000
        for i in range(Column.PIXELS):
            if self.pixels[i]:
                b |= 1 << i

        b |= self.colour
        return bytes([(b & 0xFF00) >> 8, b & 0x00FF])

    def __len__(self) -> int:
        return Column.PIXELS

    def __getitem__(self, key: int) -> bool:
        return self.pixels[key]

    def __setitem__(self, key: int, value: bool) -> None:
        self.pixels[key] = value

    def __iter__(self) -> Iterator[bool]:
        return iter(self.pixels)


class Message:
    MAX_COLUMNS = 144
    COLUMN_GROUPS = 8

    def __init__(self, columns: Optional[Sequence[Column]]=None):
        if columns:
            try:
                if not all(isinstance(x, Column) for x in columns):
                    raise ValueError("Message must be an iterable of Columns")
                elif len(columns) > Message.MAX_COLUMNS:
                    raise ValueError(f"Message must be an iterable of no more "
                                     f"than {Message.MAX_COLUMNS} Columns")
                elif len(columns) % Message.COLUMN_GROUPS != 0:
                    raise ValueError(f"Message must be an iterable with a "
                                     f"multiple of {Message.COLUMN_GROUPS} "
                                     f"columns")
            except TypeError:
                raise ValueError("Message must be an iterable of Columns")

            self.columns = list(columns)
        else:
            self.columns = [Column() for _ in range(Message.MAX_COLUMNS)]

    def __len__(self) -> int:
        return len(self.columns)

    def __getitem__(self, key: int) -> Column:
        return self.columns[key]

    def __setitem__(self, key: int, value: Column) -> None:
        self.columns[key] = value

    def __bytes__(self) -> bytes:
        # start with the program length
        # note: we always have two NUL pixels at the start and end
        program_data = bytes([len(self.columns) + 2])

        # followed by 3 + 2 NUL's (possible that some of these are the style?)
        program_data += b'\0\0\0\0\0'

        # concatenate the bytes of each column - columns are put in backwards
        program_data += b''.join(bytes(x) for x in reversed(self.columns))

        # finally, two more NUL's
        program_data += b'\0\0'

        # apply subtraction
        program_data = bytes((Program.SUBTRACTION - x) & 0xFF
                             for x in program_data)

        # build the iterable
        return program_data


class MessageIterator:
    FIRST_HEADER = b'\x00\x40\x40'
    HEADER = b'\x00\x40\x23'

    def __init__(self, data: bytes):
        self.data = data
        self._pos = 0

    def __iter__(self):
        return self

    def __next__(self) -> bytes:
        if self._pos + 5 > len(self.data):
            raise StopIteration
        elif self._pos > 0:
            message = Program.checksum(
                MessageIterator.HEADER + self.data[self._pos:self._pos + 5])
        else:
            message = Program.checksum(
                MessageIterator.FIRST_HEADER +
                self.data[self._pos:self._pos+5])
        self._pos += 5
        return message


class Program:
    SUBTRACTION = 0xA4
    MAX_MESSAGES = 7

    def __init__(self, messages: Sequence[Message]):
        if len(messages) > Program.MAX_MESSAGES:
            raise ValueError("Too many messages provided")
        self.messages = list(messages)

    @staticmethod
    def checksum(message: bytes) -> bytes:
        if not isinstance(message, bytes):
            raise ValueError("Can only checksum bytes type")
        if len(message) != 8:
            raise ValueError("Incorrect message length for checksumming")

        return message + bytes([sum(message[1:8]) & 0xFF])

    def __len__(self) -> int:
        return len(self.messages)

    def __getitem__(self, key: int) -> Message:
        return self.messages[key]

    def __setitem__(self, key: int, value: Message) -> None:
        self.messages[key] = value

    def __iter__(self):
        # first get all the program data, plus 10 NUL's to mark the end
        messages = b''.join(bytes(p) for p in self.messages) + \
                   bytes([Program.SUBTRACTION]) * 10

        # data starts with the following algorithm:
        #     max(floor(log_2(data_length) - 6), 1)
        # the program has this as a series of if's, but this is Python
        data = bytes([floor(log2(max(len(messages) >> 6, 2))),
                      len(messages) & 0x00FF,
                      (len(messages) & 0xFF00) >> 8])

        # three NUL's follow, however the 3rd NUL falls into the 2nd message,
        # which is sent under the SUBTRACTION, therefore it is 0xA4
        data += b'\0\0' + bytes([Program.SUBTRACTION])

        # next, the number of programs is sent
        data += bytes([0x24 - len(self.messages)])

        # get the data for each of the programs
        data += messages

        return MessageIterator(data)
