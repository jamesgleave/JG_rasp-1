import led_matrix_interface as Jworld
from PIL import Image, ImageDraw
# from rgbmatrix import RGBMatrix, RGBMatrixOptions
# from rgbmatrix import graphics


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
    audio_in = Jworld.JAudio.AudioStream()
    for time in range(600):
        peaks = audio_in.update()["peak"]
        print(peaks)
        Jworld.time.sleep(0.0166666)


def static_test():
    audio = Jworld.JAudio.Waveform()
    Dmatrix = audio.Dmatrix
    double_buffer = Dmatrix.CreateFrameCanvas()

    rect = Jworld.make_rect(32-10, 16-10, 32+10, 16+10, matrix=double_buffer)
    
    rect2 = Jworld.make_rect(32, 16, 32, 16, matrix=double_buffer, colour_scheme=(225,0,50))

    rect3 = Jworld.make_rect(32, 16, 32, 16, matrix=double_buffer, colour_scheme=(225,0,50))

    rect_middle = Jworld.make_rect(32-10, 16-10, 32+10, 16+10, matrix=double_buffer, colour_scheme=(255,100,0))

    last_peak = 0
    while True:
        peak = int(audio.update() * -1 * (1/(last_peak+1)))
        p1 = peak/5
        if peak > 15:
            peak = 15

        rect.update(y1=(16 + peak), y2=(16 - peak), x1=(32 + peak), x2=(32 - peak))
        
        rect2.update(y1=(16 + p1), y2=(16 - p1), x1=(52 + p1), x2=(52 - p1))
        
        rect3.update(y1=(16 + p1), y2=(16 - p1), x1=(12 + p1), x2=(12 - p1))
        
        rect_middle.update(y1=(16 + p1/2), y2=(16 - p1/2), x1=(32 + p1/2), x2=(32 - p1/2))

        if peak > last_peak:
            last_peak = peak
        if last_peak > .1:
            last_peak = last_peak * 0.99999
        else:
            last_peak = 0

        double_buffer = Dmatrix.SwapOnVSync(double_buffer)
        Jworld.time.sleep(.033333)


def composite_test():
    # This is using my personal shape library

    # Must create the matrix after the audio input to avoid seg. error
    audio = Jworld.JAudio.Waveform()
    matrix = RGBMatrix(options=Jworld.options)

    circle = Jworld.make_circle(r=5, x=32, y=16, matrix=matrix)
    last_peak = 0

    for _ in range(300):
        peak = audio.update()
        radius_update = int(last_peak)
        circle.update(r=radius_update)
        circle.build()

        print(radius_update)
        

        Jworld.time.sleep(5.01)
        matrix.Clear()

        if peak > last_peak:
            last_peak = peak
            matrix.SetPixel(32, 16, 225,0,0)

        if last_peak > .1:
            last_peak = last_peak * 0.9
        else:
            last_peak = 0


def builtin_composite_test():
    # this is using the rpi matrix library shape

    # Must create the matrix after the audio input to avoid seg. error
    audio = Jworld.JAudio.Waveform()
    matrix = RGBMatrix(options=Jworld.options)

    image = Image.new("RGB", (64, 32))  # Can be larger than matrix if wanted!!
    draw = ImageDraw.Draw(image)  # Declare Draw instance before prims
    #Draw some shapes into image (no immediate effect on matrix)...
    draw.ellipse(xy=(32, 16, 42, 26), fill=(100, 5, 100), outline=(0, 100, 0))

    last_peak = 0

    for _ in range(1000):
        peak = audio.update()
        radius_update = int(last_peak)

        draw = ImageDraw.Draw(Image.new("RGB", (64, 32)))
        draw.ellipse(xy=(22, 6, 42, 26), fill=(100, 5, 100), outline=(0, 100, 0))
        matrix.SetImage(image, 32, 16)

        Jworld.time.sleep(.3)
        matrix.Clear()

        if peak > last_peak:
            last_peak = peak

        if last_peak > .1:
            last_peak = last_peak * 0.9
        else:
            last_peak = 0


def draw_image_test():
    matrix = RGBMatrix(options=Jworld.options)
    # RGB example w/graphics prims.
    # Note, only "RGB" mode is supported currently.
    image = Image.new("RGB", (32, 32))  # Can be larger than matrix if wanted!!
    draw = ImageDraw.Draw(image)  # Declare Draw instance before prims
    # Draw some shapes into image (no immediate effect on matrix)...
    draw.rectangle((0, 0, 31, 31), fill=(0, 0, 0), outline=(0, 0, 255))
    draw.line((0, 0, 31, 31), fill=(255, 0, 0))
    draw.line((0, 31, 31, 0), fill=(0, 255, 0))

    # Then scroll image across matrix...
    for n in range(-32, 33):  # Start off top-left, move off bottom-right
        matrix.Clear()
        matrix.SetImage(image, n, n)
        Jworld.time.sleep(0.05)


def circle_solid_test():
    v = Jworld.physics_engine.Vector2
    env = Jworld.PWorld()
    circle_pos = env.add_pixel(position=v(32, 16))
    circle = Jworld.physical_objects.CirclePhysSolid(v(32, 16), 5, circle_pos)

    circle.add_force(v(10, 0))
    while True:
        env.update()


def audio_and_physics_engine_test():
    audio = Jworld.JAudio.AudioStream()
    world = Jworld.PWorld(matrix=audio.Dmatrix)

    for _ in range(25):
        world.add_pixel()

    for time in range(1000):
        peak = audio.update()["peak"]
        world.update()
        Jworld.time.sleep(0.0166666)

        if peak > 10:
            for p in world.environment.object_list:
                x = Jworld.np.random.randint(-20, 20)
                y = Jworld.np.random.randint(-20, 20)
                f = Jworld.Vector2(x, y).scalar_mult(peak)

                random_vector = Jworld.Vector2.random_vector(f)
                p.add_force(random_vector)

    world.empty()

    del audio, world

#physics_test()
#audio_test()
#static_test()
circle_solid_test()
