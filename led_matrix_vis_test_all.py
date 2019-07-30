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
    audio_in = Jworld.JAudio.Waveform()
    for time in range(600):
        audio_in.update()
        peaks = audio_in.peak
        print(peaks)
        Jworld.time.sleep(0.0166666)


def static_test():
    matrix = RGBMatrix(options=Jworld.options)
    rect = Jworld.make_rect(22, 6, 32, 16, matrix=matrix)

    for x in range(300):
        x1, y1, x2, y2 = rect.get_corners()
        rect.update(y1=(y1 + 1/60))
        Jworld.time.sleep(1/60)
        matrix.Clear()
        if y1 > 32:
            break


def composite_test():
    # This is using my personal shape library

    # Must create the matrix after the audio input to avoid seg. error
    audio = Jworld.JAudio.Waveform()
    # matrix = RGBMatrix(options=Jworld.options)

    # circle = Jworld.make_circle(5, x=32, y=16, matrix=matrix)
    last_peak = 0

    for _ in range(300):
        peak = audio.update()
        radius_update = int(last_peak)
        # print(radius_update)
        # circle.update(r=radius_update)
        for _ in range(radius_update):
            print("*", end="")

        print(radius_update)
        # print()

        Jworld.time.sleep(1/60)
        # matrix.Clear()

        if peak > last_peak:
            last_peak = peak

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
    # Draw some shapes into image (no immediate effect on matrix)...
    draw.ellipse(xy=(32, 16), fill=(100, 5, 100), outline=(0, 100, 0))

    last_peak = 0

    for _ in range(300):
        peak = audio.update()
        radius_update = int(last_peak)

        draw = ImageDraw.Draw(Image.new("RGB", (64, 32)))
        draw.ellipse(xy=(32, 16), fill=(100, 5, 100), outline=(0, 100, 0))

        matrix.Clear()
        matrix.SetImage(image, 0, 0)

        for _ in range(radius_update):
            print("*", end="")

        print(radius_update)

        Jworld.time.sleep(1/60)
        # matrix.Clear()

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

def text_test(text):
    matrix = RGBMatrix(options=Jworld.options)
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")
    textColor = graphics.Color(255, 255, 0)
    pos = offscreen_canvas.width
    my_text = text

    while True:
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)






