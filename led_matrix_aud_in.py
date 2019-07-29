"""
Notebook for streaming data from a microphone in realtime

audio is captured using pyaudio
then converted from binary data to ints using struct
then displayed using matplotlib

scipy.fftpack computes the FFT

if you don't have pyaudio, then run

# >>> pip install pyaudio

note: with 2048 samples per chunk, I'm getting 20FPS
when also running the spectrum, its about 15FPS
"""

import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
import math
import led_matrix_static_objects as shapes

# constants
CHUNK = 1024         # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100  # samples per second

p = pyaudio.PyAudio()


class Spectrogram:

    def __init__(self):
        self.y_val = []

    def start(self):
        # create matplotlib figure and axes
        fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

        # pyaudio class instance

        bar_y = []

        # stream object to get data from microphone
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK
        )

        # variable for plotting
        x = np.arange(0, 2 * CHUNK, 2)  # samples (waveform)
        xf = np.linspace(0, RATE, CHUNK)  # frequencies (spectrum)

        # create a line object with random data
        line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)

        # create semilogx line for spectrum
        line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK), '-', lw=2)

        print('stream started')

        # for measuring frame rate
        frame_count = 0
        start_time = time.time()

        while True:

            # binary data
            data = stream.read(CHUNK, exception_on_overflow=False)

            # convert data to integers, make np array, then offset it by 127
            data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

            # create np array and offset by 128
            data_np = np.array(data_int, dtype='b')[::2] + 128

            line.set_ydata(data_np)

            # compute FFT and update line
            yf = fft(data_int)
            line_fft.set_ydata(np.abs(yf[0:CHUNK]) / (128 * CHUNK))

            freq = (np.abs(yf[0:CHUNK]) / (128 * CHUNK))

            counter = 0
            ave_list = []

            for n in freq:
                ave_list.append(n)
                if counter % 32 == 0:
                    y = np.sum(ave_list, axis=0)
                    bar_y.append(sigmoid(y))

                    self.y_val = bar_y.copy()

                    ave_list = []
                counter += 1
            bar_y.clear()
            self.print_spectrogram()
            self.display()

    def print_spectrogram(self):
        for i in range(len(self.y_val)):

            print(32 - int(self.y_val[i] * 32), end=", ")
        print()

    def display(self):
        """Overridden in subclass"""


class Waveform(object):
    def __init__(self):
        self.peak = 0
        self.__start()

    def update(self):
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        peak = np.average(np.abs(data)) * 2
        bars = "#" * int(100 * peak / 2 ** 16)
        self.peak = int(500 * peak / 2 ** 16)
        self.set_matrix_height(bars)
        return self.peak

    def __start(self):
        self.update()

    def terminate(self):
        p.terminate()

    def set_matrix_height(self, bars):
        pass


def sigmoid(x):
    return 1/(1 + pow(math.e, -x))
#
# s = Waveform()
# while True:
#     print(s.update())

