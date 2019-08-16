import subprocess
import time
import sys

sys.path.insert(1, '/Users/martingleave/Documents/GitHub/JG_rasp-1')
import led_matrix_interface as Jworld
from led_matrix_interface import graphics

# initializing the pen object for writing text
pen = Jworld.Pen(canvas=Jworld.RGBMatrix(options=Jworld.options))

start_time = time.time()
delta_time = time.time() - start_time

font = graphics.Font()
font.LoadFont("../../../fonts/7x13.bdf")


while delta_time > 0:
    delta_time = 6 - int(time.time() - start_time)
    pen.draw_text(c=(225, 0, 0), font=font,
                  text="Time To Shutdown..." + str(delta_time),
                  x=0, y=16)
    time.sleep(1)
    pen.matrix.Clear()

subprocess.call(["sudo", "halt", "-p"])


