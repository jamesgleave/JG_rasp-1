import led_matrix_interface as Jworld
from rgbmatrix import RGBMatrix, RGBMatrixOptions


def functions_testing():
    physics_test()
    audio_test()


def physics_test():
    matrix = RGBMatrix(options=Jworld.options)

    world = Jworld.PWorld(matrix=matrix)
    for _ in range(25):
        world.add_pixel()

    for time in range(600):
        world.update()
        Jworld.time.sleep(0.0166666)

    world.empty()

    world.add_circle(r=5, points=20)
    for time in range(600):
        world.update()
        Jworld.time.sleep(0.0166666)
    world.empty()
    del matrix


def audio_test():
    audio_in = Jworld.JAudio.Waveform()
    for time in range(600):
        audio_in.update()
        peaks = audio_in.peak
        print(peaks)
        Jworld.time.sleep(0.0166666)


def static_test():
    matrix = RGBMatrix(options=Jworld.options)
    rect = Jworld.make_rect(22, 6, 32, 16, matrix=matrix)

    for x in range(30):
        x1, y1, x2, y2 = rect.get_corners()
        rect.update(y1=(y1 + 1/60))
        Jworld.time.sleep(1/60)
        matrix.Clear()
        if y1 > 32:
            break


def composite_test():
    # Must create the matrix after the audio input to avoid seg. error
    audio = Jworld.JAudio.Waveform()
    matrix = RGBMatrix(options=Jworld.options)

    circle = Jworld.make_circle(5, x=32, y=16, matrix=matrix)

    for _ in range(30):
        Jworld.time.sleep(1/60)








