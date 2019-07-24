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


class Matrix_simulator:
    def __init__(self, obj_list, matrix_shape=(32, 64)):
        self.r = matrix_shape[0]
        self.c = matrix_shape[1]
        self.obj_list = obj_list
        self.matrix = self.build_matrix()

    def build_matrix(self):
        matrix = []
        col = []

        for r in range(self.r):
            for c in range(self.c):
                col.append("o ")
            matrix.append(col)
        return matrix

    def position_list(self):
        pos_list = []
        for t in self.obj_list:
            pos_list.append(t.position.get_position())
        return pos_list

    def print_matrix(self):
        for r in range(self.r):
            for c in range(self.c):
                print(self.matrix[r][c], end="")
            print()
        print("\n\n\n")

    def simulate_led_matrix(self):
        for r in range(self.r):
            for c in range(self.c):
                position_tuple_list = self.position_list()
                matrix_coord = (r, c)
                if matrix_coord in position_tuple_list:
                    self.matrix[r][c] = "∆ "
                    break
                else:
                    self.matrix[r][c] = "o "
        self.print_matrix()


def physics_test(frame_rate=10):
    env = Physics()
    p = PhysicalPixel(Physics.Vector2(np.random.randint(64), np.random.randint(33)), env, matrix=Dmatrix)
    env.add(p)
    p.add_force(Physics.Vector2(0.3,0.2))
    
    init_time = time.time()
    i = 0

    while True:
        i+=1
        delta_time = time.time() - init_time

        env.update_environment()
        Dmatrix.Clear()


def frame_rate_test(fr=68):
    env = Physics(fps=fr)
    start_time = time.time()
    for _ in range(10):
        x = PhysicalPixel(position=Physics.Vector2(16, 32), environment=env, mass=.5, matrix=None)
        x.add_force(Physics.Vector2(np.random.sample() * 100, np.random.sample() * 100))
        env.add(x)

    i = 0
    frames_passed = 0

    matrix = Matrix_simulator(env.get_object_list())
    while True:
        env.update_environment()
        delta_time = time.time() - start_time
        matrix.simulate_led_matrix()

        frames_passed += 1
        i += 1


frame_rate_test()
Dmatrix.Clear()
        
    
    
    
    

