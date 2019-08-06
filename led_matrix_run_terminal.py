import led_matrix_interface as Jworld
from Displays import audio_visualizer_one, Spectrogram_BouncingBoxes

"""This is used to interact with the app.py file. This will run all files activated remotely or """


class RunTerminal:

    @staticmethod
    def run_program(program, message=None):
        rows, cols = Jworld.rows, Jworld.cols
        if program == "BouncingBoxes":
            Spectrogram_BouncingBoxes.run_spectrogram(cols, rows)
        elif program == "Staggering":
            audio_visualizer_one.run_visualizer(cols, rows)
        elif program == "text":
            pass
            # TODO implement sliding text, static text, and physical text.


# Main function
if __name__ == "__main__":
    terminal = RunTerminal()
    terminal.run_program(program="BouncingBoxes")
