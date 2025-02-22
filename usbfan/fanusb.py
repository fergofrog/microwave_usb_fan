import hid
import usb.core


from usbfan.protocol import Program

def try_open_hid_based_device():
    try:
        device = hid.device()
        device.open(0x0c45, 0x7160)
        return device
    except Exception as e:
        print("Failed to open HID device. Do you have permission to access the device?", e)
        return None

def try_open_usb_based_device():
    try:
        usbdevice = usb.core.find(idVendor=0x1a86, idProduct=0x5537)
        if usbdevice is None:
            raise Exception("Device 1a86:5537 not found")
        print("Found device 1a86:5537")
        usbdevice.set_configuration()
        return usbdevice
    except Exception as e:
        print("Failed to open USB device. Do you have permission to access the device?", e)
        return None


class AdapterDevice:

    def __init__(self, usbdevice):
        self.usbdevice = usbdevice

    def write(self, message):

        print(f"Writing {len(message)} bytes to the device: {message.hex()}")
        self.usbdevice.write(0x02, message)

    def read(self, length):
        return self.usbdevice.read(0x82, length)


class Device:
    def __init__(self, vendor_id=0x0c45, product_id=0x7160):
        usbdevice = try_open_usb_based_device()  # The older devices
        if usbdevice is not None:
            self.device = AdapterDevice(usbdevice)
            self.truncate_leading_zero = True
            self.ack = b'\x40\x24\x80'
            return

        print("Failed to open USB device. Trying HID device.")
        hiddevice = try_open_hid_based_device()
        if hiddevice is not None:
            self.device = hiddevice
            self.truncate_leading_zero = False
            self.ack = b'\x24\x80'
            return

        raise Exception("Failed to open any device")


    def program(self, program: Program):
        print("Programming the device")
        if not isinstance(program, Program):
            raise ValueError("need a Program to program the device")

        for message in program:
            if self.truncate_leading_zero and len(message) > 8:
                message = message[1:]
            self.device.write(message)

            ack = bytes(self.device.read(len(self.ack)))
            if ack != self.ack:
                print("Got an error on upload: %s" % ack.hex())


if __name__ == "__main__":
    from usbfan.message import TextMessage

    f = Program((TextMessage("Hello, World!"),
                 TextMessage("How is everyone going?"),))
    d = Device()
    d.program(f)
