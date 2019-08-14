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

# from rgbmatrix import RGBMatrix, RGBMatrixOptions

# options = RGBMatrixOptions()
# options.rows = 32
# options.cols = 64
# options.chain_length = 1
# options.parallel = 1
# options.hardware_mapping = 'adafruit-hat'

import pyaudio
import os
import struct
import numpy as np
from scipy.fftpack import fft
import time
import math
import led_matrix_interface as Jworld


# constants
CHUNK = 1024         # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second


class Spectrogram:
    def __init__(self):
        self.y_val = []
        self.stream = None
        self.Dmatrix = None
        self.start()

    def start(self):
        # pyaudio class instance
        p = pyaudio.PyAudio()
        
        # stream object to get data from microphone
        self.stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            frames_per_buffer=CHUNK,
            input_device_index=1,
            input=True,
        )
        
        self.Dmatrix = RGBMatrix(options=options)

        print('stream started')
        
    def update_matrix(self):
        Dmatrix = self.Dmatrix
        Dmatrix.Clear()
        for x in range(64):
            bar_y = int((self.y_val[int(x/4)]) * 32) - 20
                
            for y in range(32):
                
                if y <= bar_y:
                    Dmatrix.SetPixel(x, y, y*6,100,x*2)
                else:
                    break
                
        time.sleep(0.0166666)
        
    def display(self):
        stream = self.stream
        bar_y = []

        # binary data
        data = stream.read(CHUNK, exception_on_overflow=False)

        # convert data to integers, make np array, then offset it by 127
        data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

        # create np array and offset by 128
        data_np = np.array(data_int, dtype='b')[::2] + 128
        # compute FFT and update line
        yf = fft(data_int)
        freq = (np.abs(yf[0:CHUNK]) / (128 * CHUNK))

        counter = 0
        ave_list = []

        for n in freq:
            ave_list.append(n)
            if counter % 64 == 0:
                y = np.sum(ave_list, axis=0)
                bar_y.append((y))

                self.y_val = bar_y[:]

                ave_list = []
            counter += 1
        clear(bar_y)
        self.update_matrix()


class Waveform:
    def __init__(self):
        self.Dmatrix = None
        self.peak = 0
        self.stream = None        
        self.__start()
        
    def update(self):

        data = np.fromstring(self.stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        peak = np.average(np.abs(data)) * 2
        self.peak = int(500 * peak / 2 ** 16)
       
        return self.peak

    def __start(self):
        # pyaudio class instance
        p = pyaudio.PyAudio()
        
        # stream object to get data from microphone
        self.stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            frames_per_buffer=CHUNK,
            input_device_index=0,
            input=True,
        )
        
        # self.Dmatrix = RGBMatrix(Jworld.options=options)

        print('stream started')

    def terminate(self, p):
        p.terminate()


class AudioStream:
    """
    Audio gets both the fft and waveform
    simultaneously. The update function returns
    a dictionary of "peak"s and a list of
    "spectrum" values.
    """
    def __init__(self):
        self.spectrum = []
        self.peak = 0
        self.stream = None
        self.Dmatrix = None
        self.__start()

    def __start(self):
        # pyaudio class instance
        p = pyaudio.PyAudio()

        # stream object to get data from microphone
        self.stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            frames_per_buffer=CHUNK,
            input_device_index=0,
            input=True,
        )

        # self.Dmatrix = RGBMatrix(options=Jworld.options)

        print('stream started')

    def update(self):
        spectrum_values = []

        # binary data
        data = np.fromstring(self.stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        peak = np.average(np.abs(data)) * 2
        self.peak = int(500 * peak / 2 ** 16)

        # convert data to integers, make np array, then offset it by 127
        # data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
        # print(len(data))

        # compute FFT and update line
        yf = fft(data)
        freq = (np.abs(yf[0:CHUNK]) / (128 * CHUNK))

        split_number = 0  # determines the amount of different frequencies we average
        ave_list = []

        for n in freq:
            ave_list.append(n)
            if split_number % 16 == 0:
                specific_spectrum_value = np.sum(ave_list, axis=0)
                spectrum_values.append(specific_spectrum_value)

                self.spectrum = spectrum_values[:]

                ave_list = []
            split_number += 1
        clear(spectrum_values)
        return {"peak": self.peak, "spectrum": self.spectrum}


def sigmoid(x):
    return 1/(1 + pow(math.e, -x))


def clear(list):
    del list[:]


def run():
    a = AudioStream()
    while True:
        pass
        list = a.update()["spectrum"][::8]
        print_list = []
        for i in list:
            print_list.append((int(10*i)))
        print(print_list)