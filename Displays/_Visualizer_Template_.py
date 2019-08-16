import led_matrix_interface as Jworld
import random
import time


def run_visualizer(matrix_length=64, matrix_height=32, time_limited=False, max_time=60):
    audio = Jworld.JAudio.Waveform()
    Dmatrix = audio.Dmatrix
    pen = Jworld.Pen(canvas=Dmatrix)

    initial_time = time.time()

    run = True

    while run:
        # Do stuff

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






