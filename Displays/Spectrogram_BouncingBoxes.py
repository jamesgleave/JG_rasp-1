import led_matrix_interface as Jworld
import random

def run_spectrogram(matrix_length, matrix_height):
    audio = Jworld.JAudio.AudioStream()
    Dmatrix = audio.Dmatrix
    pen = Jworld.Pen(canvas=Dmatrix)

    x_pos = 0
    y_pos = 0

    r_colour_thresh = 0
    g_colour_thresh = 0
    b_colour_thresh = 0

    x_increment = 8  # length / number of boxes

    while True:
        spectrum_values = audio.update()["spectrum"][::8]  # 8 boxes
        waveform_values = audio.update()["peak"]

        while x_pos > matrix_height:
            y_pos = spectrum_values[x_pos/x_increment]  # gets the value of the spectrogram

            r_colour_thresh = waveform_values

            colour = (r_colour_thresh, g_colour_thresh, b_colour_thresh)
            pen.draw_rect(x_pos + 2, y_pos + 2, x_pos + 4, y_pos + 4, colour, fill=True)
            x_pos += x_increment

