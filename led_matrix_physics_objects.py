"""

All of these classes are used to generate objects that are effected by physics from led_matrix_physics.

From these geometric shapes, any complex shape should be possible to create!

"""


from led_matrix_physics import Physics, PhysicalPixel, RandomPhysicalPixel, Vector2, ForceEmitter
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


class CirclePhysComp:
    def __init__(self, pos, r, points, physical_pixel, fill=False):

        self.physical_pixel = physical_pixel

        self.r = r
        self.position = pos
        self.points = points
        self.point_list = []

        if not fill:
            self.build()
        else:
            self.fill_build()

    def build(self):
        # r^2 = x^2 + y^2
        # r^2 - x^2 = y^2
        # squrt(r^2 - x^2) = +-y

        r = self.r
        x = -r
        step_size = int(2*r / self.points)

        while x <= r:

            y = np.sqrt(pow(r, 2) - pow(x, 2))

            y = round(y)

            pos = self.physical_pixel.clone()
            pos.position.x, pos.position.y = self.position.x + x, self.position.y + y
            self.point_list.append(pos)

            neg = self.physical_pixel.clone()
            neg.position.x, neg.position.y = self.position.x + x, self.position.y - y
            self.point_list.append(neg)

            x += step_size

    def fill_build(self):
        # r^2 = x^2 + y^2
        # r^2 - x^2 = y^2
        # squrt(r^2 - x^2) = +-y

        r = self.r

        while r != 0:

            x = -r
            while x <= r:

                y = np.sqrt(pow(r, 2) - pow(x, 2))

                pos = self.physical_pixel.clone()
                pos.position.x, pos.position.y = self.position.x + x, self.position.y + y
                self.point_list.append(pos)

                neg = self.physical_pixel.clone()
                neg.position.x, neg.position.y = self.position.x + x, self.position.y - y
                self.point_list.append(neg)

                x += 1
            r -= 1

    def add_force(self, f):
        force = Vector2(f.x, f.y)
        for p in self.point_list:
            p.add_force(force)


class RectPhysComp:
    # TODO implement this class
    pass


class LinePhysComp:
    # TODO implement this class
    pass


class TriPhysComp:
    # TODO implement this class
    pass


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
                        self.matrix[r][c] = "@ "
                        break
                    else:
                        self.matrix[r][c] = "- "

        self.print_matrix()


def frame_rate_test(fr=1000):
    env = Physics(fps=fr, air_resistance=0.97)
    start_time = time.time()

    # for i in range(20):
    #     x = PhysicalPixel(position=Vector2(i, 16),
    #                       environment=env, mass=np.random.randint(1, 10), matrix=None)
    #     env.add(x)

    x = PhysicalPixel(position=Vector2(32, 16),
                      environment=env,
                      matrix=None)

    fe = ForceEmitter(5000, 30, env.object_list)

    circle = CirclePhysComp(Vector2(32, 10), r=10, points=10, physical_pixel=x)
    env.add_physical_body(circle)

    fe.detonate(Vector2(32, 16))

    env.update_environment()
    matrix = MatrixSimulator(env.get_object_list())
    matrix.simulate_led_matrix()

    i = 0
    frames_passed = 0
    delta_time = time.time() - start_time

    while True:
        env.update_environment()
        delta_time = time.time() - start_time
        matrix.simulate_led_matrix()

        frames_passed += 1
        i += 1
        if i % 100 == 0:
            env.clear()
            circle = CirclePhysComp(Vector2(32, 10), r=3, points=10, physical_pixel=x, fill=True)

            env.add_physical_body(circle)
            rand1 = np.random.sample() * np.random.randint(-1, 2) * 20000
            rand2 = np.random.sample() * np.random.randint(-1, 2) * 30000
            env.update_environment()
            matrix.simulate_led_matrix()

            time.sleep(1)
            circle.add_force(Vector2(rand1, rand2))


# frame_rate_test()
# Dmatrix.Clear()

        
    
    
    
    

