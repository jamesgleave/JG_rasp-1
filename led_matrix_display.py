from rgbmatrix import RGBMatrix, RGBMatrixOptions
import led_matrix_physics as physics
import numpy as np
import time

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
Dmatrix = RGBMatrix(options=options)
Dmatrix.Clear()


class Bar():
    def __init__(self, width, x, color_scheme=None):
        self.w = width
        self.x = x
        
        if color_scheme != None:
            print("do something")
        
        self.build()
        
    def build(self, y=0):
        r,g,b = 0,0,100
        
        for x_bar in range(self.w):
            for y_bar in range(y):
                r = y * 8 
                g = x_bar * 45
                
                Dmatrix.SetPixel(x_bar + self.x, y_bar, r, g, b)


class Circle():
    def __init__(self, x, y ,r):
        self.x = x
        self.y = y
        self.r = r

        self.build(x, y, r)

    def build(self, x, y, r):
        return x


bar_list = []
w = 5
for i in range(64):
    
    if i % w == 0:
        bar_list.append(Bar(w,i))            
        
while True:
    i = 0
    time.sleep(0.1)
    Dmatrix.Clear()
    for bar in bar_list:
        i += bar.x
        bar.build(int(np.random.sample() * 32))
    
