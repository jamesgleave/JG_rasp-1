import time
import sys

sys.path.insert(1, '/Users/martingleave/Documents/GitHub/JG_rasp-1')
import led_matrix_interface as Jworld
from led_matrix_interface import graphics


def display_message(message):
    # initializing the pen object for writing text
    pen = Jworld.Pen(canvas=Jworld.RGBMatrix(options=Jworld.options))
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")

    x = 64
    while True:
        pen.matrix.Clear()
        len = pen.draw_text(c=(225, 0, 0), font=font,
                            text=message,
                            x=0, y=0)

        time.sleep(.03)
        x -= 1
        if x + len < 0:
            break


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--message")
    args = parser.parse_args()
    display_message(args.message)
