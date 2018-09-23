import hid

from usbfan.protocol import Program


class Device:
    def __init__(self, vendor_id=0x0c45, product_id=0x7160):
        self.device = hid.device()
        self.device.open(vendor_id, product_id)

    def program(self, program: Program):
        if not isinstance(program, Program):
            raise ValueError("need a Program to program the device")

        for message in program:
            self.device.write(message)
            ack = bytes(self.device.read(3))
            if ack != b'\x24\x80':
                print("Got an error on upload")


if __name__ == "__main__":
    from usbfan.message import TextMessage

    f = Program((TextMessage("Hello, World!"),
                 TextMessage("How is everyone going?"),))
    d = Device()
    d.program(f)
