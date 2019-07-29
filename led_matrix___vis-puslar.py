import led_matrix_interface as JWorld

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
        j = JWorld.PWorld()
        j.add_pixel(matrix=self.Dmatrix)

        while True:
            peak = self.aud_in.update()
            JWorld.make_circle(peak, 32, 16, matrix=self.Dmatrix)
            Dmatrix.Clear()
            Dmatrix = RGBMatrix(options=options)
            Dmatrix.Clear()


if __name__ == '__main__':
    pulsar = Pulsar()
    pulsar.run()



