from threading import Lock
from bottle import route, run, response, request
from usbfan import Device, Program, Message, TextMessage, Column, Colour


dev_lock = Lock()
dev = Device()


@route('/', method='OPTIONS')
def options():
    response.set_header("Access-Control-Allow-Origin", "http://localhost:8000")
    response.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.set_header("Access-Control-Allow-Headers", "accept, content-type")
    response.set_header("Access-Control-Max-Age", "1728000")
    return ''


@route('/', method='POST')
def change_slide_event():
    global dev, dev_lock

    slide = request.json['indexh']
    print("Slide {}".format(slide))

    p = None
    if slide == 2:
        # Slide 2: "This" - "Hello CSides" - "Fri 19 Oct 2018"
        p = Program((
            TextMessage("This!"),
            TextMessage("Hello CSides"),
            TextMessage("Fri 19 Oct 18"),
        ))
    elif slide == 37:
        # Slide 37: "Single Red Dot"
        columns = [Column([True] + [False] * 10, Colour.red)]
        for _ in range(7):
            columns.append(Column([False] * 11, Colour.red))
        p = Program((Message(columns),))
    elif slide == 44:
        # Slide 44: "Two Red Dots"
        columns = list()
        columns.append(Column([True] + [False] * 10, Colour.red))
        columns.append(Column([True] + [False] * 10, Colour.red))
        for _ in range(6):
            columns.append(Column([False] * 11, Colour.red))
        p = Program((Message(columns),))
    elif slide == 47:
        # Slide 47: "Full Vertical Red"
        columns = [Column([True] * 11, Colour.red)]
        for _ in range(7):
            columns.append(Column([False] * 11, Colour.red))
        p = Program((Message(columns),))
    elif slide == 49:
        # Slide 49: "Full Vertical Blue"
        columns = [Column([True] * 11, Colour.blue)]
        for _ in range(7):
            columns.append(Column([False] * 11, Colour.red))
        p = Program((Message(columns),))
    elif slide == 51:
        # Slide 51: "Full Vertical Green"
        columns = [Column([True] * 11, Colour.green)]
        for _ in range(7):
            columns.append(Column([False] * 11, Colour.red))
        p = Program((Message(columns),))
    elif slide == 61:
        # Slide 61: "Questions?" - RAINBOW!
        rainbow_colours = [Colour.red, Colour.yellow, Colour.green,
                           Colour.cyan, Colour.blue, Colour.magenta]
        rainbow = [Column([True] * 11,
                          rainbow_colours[i % len(rainbow_colours)])
                   for i in range(Message.MAX_COLUMNS)]
        p = Program((
            TextMessage("Questions?"),
            Message(rainbow),
        ))

    if p:
        with dev_lock:
            dev.program(p)

    return ''


def main():
    run(host='localhost', port=8080)


if __name__ == "__main__":
    main()
