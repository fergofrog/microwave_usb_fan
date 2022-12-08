from os.path import dirname, join

from PIL import Image, ImageDraw, ImageFont

from .protocol import Colour, ColourTheme, Column, Message, MessageStyle, OpenTransition, \
    CloseTransition


class TextMessage(Message):
    def __init__(self, text: str,
                 message_style: MessageStyle=MessageStyle.Anticlockwise,
                 colour: Colour=Colour.white,
                 theme: ColourTheme=ColourTheme.single,
                 open_transition: OpenTransition=OpenTransition.LeftRight,
                 close_transition: CloseTransition=CloseTransition.RightLeft):
        # Open the font, create a blank image and an ImageDraw object
        fnt = ImageFont.truetype(
            #join(dirname(__file__), 'fonts', '/usr/share/fonts/liberation-mono/LiberationMono-Bold.ttf'))
            join(dirname(__file__), 'fonts', 'Hack-Regular.ttf'))
        img = Image.new('RGB', (Message.MAX_COLUMNS, Column.PIXELS))
        d = ImageDraw.Draw(img)

        # Array of colours for each column.  
        # The hardware can only support one colour per column so our colour resolution is 1-dimensional (horizontal, never vertical)
        colours = [0] * Message.MAX_COLUMNS
        for column in range( Message.MAX_COLUMNS ):
            
            if theme == ColourTheme.Ice:
                if column % 20 < 4:
                    colours[column] = Colour.cyan
                elif column % 20 < 6:
                    colours[column] = Colour.white
                elif column % 20 < 10:
                    colours[column] = Colour.cyan
                else:
                    colours[column] = Colour.blue

            elif theme == ColourTheme.Festive:
                if column % 30 < 6:
                    colours[column] = Colour.blue
                elif column % 30 < 12:
                    colours[column] = Colour.magenta
                elif column % 30 < 18:
                    colours[column] = Colour.red
                elif column % 30 < 24:
                    colours[column] = Colour.yellow
                else:
                    colours[column] = Colour.green

            elif theme == ColourTheme.Fire:
                if column % 5 == 2:
                    colours[column] = Colour.yellow
                else:
                    colours[column] = Colour.red

            elif theme == ColourTheme.Christmas:
                if column % 40 < 10:
                    colours[column] = Colour.green
                elif column % 40 < 20:
                    colours[column] = Colour.red
                elif column % 40 < 30:
                    colours[column] = Colour.green
                else:
                    colours[column] = Colour.red

            elif theme == ColourTheme.Rainbow:
                if column % 20 < 4:
                    colours[column] = Colour.red
                elif column % 20 < 8:
                    colours[column] = Colour.yellow
                elif column % 20 < 12:
                    colours[column] = Colour.green
                elif column % 20 < 16:
                    colours[column] = Colour.cyan
                else:
                    colours[column] = Colour.blue

            else:
                colours[column] = colour;


        # Write the text into the image
        d.text((0, -1), text, font=fnt)

        # Transpose the image
        img = img.transpose(Image.TRANSPOSE)

        # Convert the image into one channel
        img_data = [True if p >= 128 else False for p in
                    img.convert('L').getdata(0)]

        # Convert the image into its columns
        columns = [Column(img_data[i:i+Column.PIXELS], colours[i//Column.PIXELS]) for i in
                   range(0, len(img_data), Column.PIXELS)]

        super().__init__(columns, message_style, open_transition,
                         close_transition)
