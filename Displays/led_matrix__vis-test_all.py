import led_matrix_interface as Jworld
# from rgbmatrix import RGBMatrix, RGBMatrixOptions


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
    rect = Jworld.make_rect(5, 32, 10, matrix)







