from os.path import dirname, join

from PIL import Image, ImageDraw, ImageFont

from .protocol import Colour, Column, Message, MessageStyle, OpenTransition, \
    CloseTransition


class TextMessage(Message):
    def __init__(self, text: str,
                 message_style: MessageStyle=MessageStyle.Anticlockwise,
                 open_transition: OpenTransition=OpenTransition.LeftRight,
                 close_transition: CloseTransition=CloseTransition.RightLeft):
        # Open the font, create a blank image and an ImageDraw object
        fnt = ImageFont.truetype(
            join(dirname(__file__), 'fonts', 'Hack-Regular.ttf'))
        img = Image.new('RGB', (Message.MAX_COLUMNS, Column.PIXELS))
        d = ImageDraw.Draw(img)

        # Write the text into the image
        d.text((0, -1), text, font=fnt)

        # Transpose the image
        img = img.transpose(Image.TRANSPOSE)

        # Convert the image into one channel
        img_data = [True if p >= 128 else False for p in
                    img.convert('L').getdata(0)]

        # Convert the image into its columns
        columns = [Column(img_data[i:i+Column.PIXELS], Colour.white) for i in
                   range(0, len(img_data), Column.PIXELS)]

        super().__init__(columns, message_style, open_transition,
                         close_transition)
