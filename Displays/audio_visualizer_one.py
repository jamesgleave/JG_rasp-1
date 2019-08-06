import led_matrix_interface as Jworld
import random


def run_visualizer(matrix_length, matrix_height):
    audio = Jworld.JAudio.Waveform()
    Dmatrix = audio.Dmatrix
    pen = Jworld.Pen(canvas=Dmatrix)

    updates_over_threshold = 0
    while True:
        peak = int(10 * Jworld.np.log(audio.update() + 1))
        pen.draw_rect(32 + peak, 16 + peak, 32 - peak, 16 - peak, (50, 50, 50), fill=True, gradient="r_grad_x")

        pen.draw_line(32, 16, 32 + peak * 2, peak * 2, (peak, 0, 0))
        pen.draw_line(32, 16, 32 - peak * 2, peak * 2, (peak, 0, 0))

        pen.draw_line(32, 16, 32 + peak * 2, 32 - peak * 2, (peak, 0, 0))
        pen.draw_line(32, 16, 32 - peak * 2, 32 - peak * 2, (peak, 0, 0))

        for n in range(peak):
            x = random.randint(0, 65)
            y = random.randint(0, 33)
            Dmatrix.SetPixel(x, y)

        if peak > 20:
            updates_over_threshold += 1
        else:
            updates_over_threshold -= 1

        for n in range(updates_over_threshold):
            x1 = random.randint(0, 65)
            y1 = random.randint(0, 33)

            x2 = random.randint(x1 - 5, x1 + 5)
            y2 = random.randint(y1 - 5, y1 + 5)

            pen.draw_rect(x1, y1, x2, y2, (50, 50, updates_over_threshold if updates_over_threshold < 225 else 225)
                          , fill=True, gradient="r_grad_x")

        Dmatrix.Clear()






