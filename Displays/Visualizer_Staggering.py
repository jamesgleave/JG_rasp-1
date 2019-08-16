import led_matrix_interface as Jworld
import random
import time


def run_visualizer(matrix_length=64, matrix_height=32, time_limited=False, max_time=60):
    audio = Jworld.JAudio.Waveform()
    Dmatrix = audio.Dmatrix
    pen = Jworld.Pen(canvas=Dmatrix)

    initial_time = time.time()

    run = True

    updates_over_threshold = 0
    while run:
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

        if time_limited:
            delta_time = int(time.time() - initial_time)
            if delta_time > max_time:
                while Dmatrix.brightness > 5:
                    Dmatrix.brightness -= 1
                    time.sleep(.01)
                run = False


# Main function
if __name__ == "__main__":
    run_visualizer(Jworld.options.cols, Jworld.options.rows)






