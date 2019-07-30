import led_matrix_interface as JWorld
import sys

options = JWorld.RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'


class Pulsar:
    def __init__(self):
        self.peak = 0
        self.aud_in = JWorld.JAudio.Waveform()

        self.Dmatrix = JWorld.RGBMatrix(options=options)
        self.Dmatrix.Clear()

    def run(self):

        while True:
            peak = self.aud_in.update()
            print(peak)
            JWorld.make_circle(peak, 32, 16, matrix=self.Dmatrix)
            Dmatrix.Clear()
            Dmatrix = RGBMatrix(options=options)
            Dmatrix.Clear()


if __name__ == '__main__':
    try:
        # Start loop
        print("Press CTRL-C to stop sample")
        pulsar = Pulsar()
        pulsar.run()
    except KeyboardInterrupt:
        print("Exiting\n")
        sys.exit(0)



