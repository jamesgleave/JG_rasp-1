from . import Spectrogram_BouncingBoxes, Visualizer_Staggering
import time


def _run_all_():
    display_list = [Spectrogram_BouncingBoxes,
                    Visualizer_Staggering]

    initial_time = time.time()
    delta_time = initial_time - time.time()

    while True:
        for display in display_list:
            display.run_visualizer(64, 32, True, 60)
