from led_matrix_physics import Physics, PhysicalPixel
import numpy as np
import time

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions

    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    Dmatrix = RGBMatrix(options=options)
    Dmatrix.Clear()

except ImportError:
    print("The package rgbmatrix was not found")


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


def bar_test():
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

class MatrixSimulator:
    def __init__(self, obj_list, matrix_shape=(32, 64)):
        self.r = matrix_shape[0]
        self.c = matrix_shape[1]
        self.obj_list = obj_list
        self.matrix = self.build_matrix()

    def build_matrix(self):
        matrix = []

        for r in range(self.r):
            col = []
            for c in range(self.c):
                col.append("• ")
            matrix.append(col)
        return matrix

    def position_list(self):
        pos_list = []
        for t in self.obj_list:
            pos_list.append(t.position.get_position())
        return pos_list

    def print_matrix(self):
        print("\n\n\n\n\n\n")

        for r in range(self.r):
            for c in range(self.c):
                print(self.matrix[r][c], end="")
            print()

    def simulate_led_matrix(self):
        for r in range(self.r):
            for c in range(self.c):
                position_tuple_list = self.position_list()
                matrix_coord = (c, r)

                for coord in position_tuple_list:
                    if Physics.occupies_same_space(coord, matrix_coord):
                        self.matrix[r][c] = "X "
                        break
                    else:
                        self.matrix[r][c] = "• "

        self.print_matrix()


def frame_rate_test(fr=68):
    env = Physics(fps=fr)
    start_time = time.time()
    for _ in range(10):
        x = PhysicalPixel(position=Physics.Vector2(32, 16),
                          environment=env, mass=10, matrix=None)
        env.add(x)

    i = 0
    frames_passed = 0

    matrix = MatrixSimulator(env.get_object_list())
    matrix.print_matrix()

    for obj in env.object_list:
        obj.add_force(Physics.Vector2(np.random.uniform(-5000, 5000), np.random.uniform(-5000, 5000)))

    time.sleep(2)
    while True:
        env.update_environment()
        delta_time = time.time() - start_time
        matrix.simulate_led_matrix()

        frames_passed += 1
        i += 1


frame_rate_test()
Dmatrix.Clear()
        
    
    
    
    

