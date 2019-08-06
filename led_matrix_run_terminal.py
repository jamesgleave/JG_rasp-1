import led_matrix_interface as Jworld
from Displays import audio_visualizer_one, Spectrogram_BouncingBoxes

"""This is used to interact with the app.py file. This will run all files activated remotely"""


class RunTerminal:

    @staticmethod
    def run_program(program, message=None):
        if program == "BouncingBoxes":
            Spectrogram_BouncingBoxes.run_spectrogram(Jworld.options.cols, Jworld.options.rows)
        elif program == "Staggering":
            audio_visualizer_one.run_visualizer(Jworld.options.cols, Jworld.options.rows)
        elif program == "text":
            pass
            # TODO implement sliding text, static text, and physical text.

