import math
import time
import led_matrix_interface as Jworld


def rotate(x, y, angle):
    return {
        "new_x": x * math.cos(angle) - y * math.sin(angle),
        "new_y": x * math.sin(angle) + y * math.cos(angle)
    }


def scale_col(val, lo, hi):
    if val < lo:
        return 0
    if val > hi:
        return 255
    return 255 * (val - lo) / (hi - lo)


def run_visualizer(matrix_length=64, matrix_height=32, time_limited=False, max_time=60):
    audio = Jworld.JAudio.Waveform()
    matrix = audio.Dmatrix
    pen = Jworld.Pen(canvas=matrix)

    initial_time = time.time()

    run = True

    cent_x = matrix.width / 2
    cent_y = matrix.height / 2

    rotate_square = min(matrix.width, matrix.height) * 1.41
    min_rotate = cent_x - rotate_square / 2
    max_rotate = cent_x + rotate_square / 2

    display_square = min(matrix.width, matrix.height) * 0.7
    min_display = cent_x - display_square / 2
    max_display = cent_x + display_square / 2

    deg_to_rad = 2 * 3.14159265 / 360
    rotation = 0
    offset_canvas = matrix.CreateFrameCanvas()

    while run:
        rotation += 1
        rotation %= 360

        for x in range(int(min_rotate), int(max_rotate)):
            for y in range(int(min_rotate), int(max_rotate)):
                ret = rotate(x - cent_x, y - cent_x, deg_to_rad * rotation)
                rot_x = ret["new_x"]
                rot_y = ret["new_y"]

                if x >= min_display and x < max_display and y >= min_display and y < max_display:
                    offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y,
                                           scale_col(x, min_display, max_display),
                                           255 - scale_col(y, min_display, max_display),
                                           scale_col(y, min_display, max_display))
                else:
                    offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)

        offset_canvas = matrix.SwapOnVSync(offset_canvas)

        if time_limited:
            delta_time = int(time.time() - initial_time)
            if delta_time > max_time:
                while matrix.brightness > 5:
                    matrix.brightness -= 1
                    time.sleep(.01)
                run = False
