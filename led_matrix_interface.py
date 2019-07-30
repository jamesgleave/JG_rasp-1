import led_matrix_physics_objects as physics_engine
from led_matrix_physics_objects import Vector2
import led_matrix_static_objects
import led_matrix_aud_in as JAudio
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

    # Dmatrix = RGBMatrix(options=options)
    # Dmatrix.Clear()

except ImportError:
    print("The package rgbmatrix was not found")


class PWorld:

    def __init__(self, air_resistance=0.95, g=.5, fps=60, matrix=None):
        """Summary of Construction

        Parameters:
        air_resistance (float): A float between 1 and 0 relating to the rate of negative acceleration experienced by
        a physical pixel. The higher the value, the longer the object remains in motion.

        g (float): The gravity of the world

        fps (int): The timescale of the world.

        matrix (RGBMatrix): Where the world will be shown

       """

        self.environment = physics_engine.Physics(air_resistance=air_resistance, g=g, fps=fps)

        self.simulated_matrix = None

        self.matrix = matrix

    def add_pixel(self, environment=None, position=None,
                  mass=None, matrix=None, c=None, velocity=None,
                  led_size=(64, 32), bounciness=None, gravity_enabled=True) -> physics_engine.PhysicalPixel:

        """Summary of method

        Parameters:
        environment (physics_engine.Physics): This is the world this object lives in. It can be left empty and is
        initialized with the classes self.environment

        position (physics_engine.Vector2): This can be left blank to be randomized, but can also be explicitly provided

        mass (int): The mass of the pixel

        matrix (RGBMatrix): This is required for any led use if none was passed to the PWorld.

        c (Tuple): The (r, g, b) values of the pixel

        led_size (Tuple): the x and y scale of the matrix

        bounciness (bounciness): The bounciness of the pixel

        gravity_enabled (bool): Enables gravity to effect the pixel


       """
        
        if environment is None:
            environment = self.environment

        if matrix is None:
            matrix = self.matrix

        if position is None:
            position = Vector2.random_vector()
        if mass is None:
            mass = np.random.randint(1, 10)

        if c is None:
            c = (0, 100, 0)
        elif c == 'rand':
            R = np.random.randint
            r, g, b = R(0, 226), R(0, 226), R(0, 226)
            c = (r, g, b)

        if bounciness is None:
            bounciness = np.random.sample()

        return self.environment.add(physics_engine.PhysicalPixel(position, environment, mass, matrix, c, velocity,
                                    led_size, bounciness, gravity_enabled))

    def add_circle(self, r, points, pos=None, environment=None,
                   mass=None, matrix=None, c=None, led_size=(64, 32),
                   bounciness=None, gravity_enabled=True, fill=False):

        """Summary of method

        Parameters:
        pos (physics_engine.Vector2): This can be left blank, but can also be explicitly provided. Default is (32,16)

        r (int): The circles radius

        points (int): The amount of pixels to make the circle out of.

        environment (physics_engine.Physics): This is the world this object lives in. It can be left empty and is
        initialized with the classes self.environment

        mass (int): The mass of the pixel

        matrix (RGBMatrix): This is required for any led use if none was passed to the PWorld.

        c (Tuple): The (r, g, b) values of the pixel

        led_size (Tuple): the x and y scale of the matrix

        bounciness (bounciness): The bounciness of the pixel

        gravity_enabled (bool): Enables gravity to effect the pixel


       """

        if environment is None:
            environment = self.environment

        if pos is None:
            pos = Vector2(32, 16)

        if matrix is None:
            matrix = self.matrix

        if mass is None:
            mass = np.random.randint(1, 10)

        if c is None:
            c = (0, 100, 0)
        elif c == 'rand':
            R = np.random.randint
            r, g, b = R(0, 226), R(0, 226), R(0, 226)
            c = (r, g, b)

        if bounciness is None:
            bounciness = np.random.sample()

        physical_pixel = physics_engine.PhysicalPixel(environment=environment, mass=mass, matrix=matrix, c=c,
                                                      led_size=led_size, bounciness=bounciness,
                                                      gravity_enabled=gravity_enabled, position=Vector2.random_vector())

        return self.environment.add_physical_body(physics_engine.CirclePhysComp(pos, r, points, physical_pixel, fill))

    def update(self):

        """Summary of method
        This updates the environment in the PWorld class. This updates all the pixels and the display.

        """
        self.environment.update_environment()

        if self.simulated_matrix is not None:
            self.simulated_matrix.simulate_led_matrix()

    def simulate_led_matrix(self):
        self.simulated_matrix = physics_engine.MatrixSimulator(self.environment.object_list)

    def empty(self):
        """Summary of method
        This clears the contents within self.environment"""
        self.environment.clear()

    def print_all_physical_object_positions(self):
        for i in self.environment.get_object_list():
            Vector2.print_vector(i.position)


def make_circle(r, x, y, matrix, colour_scheme=None, gradient=None, fill=True):
    return led_matrix_static_objects.Circle(r, x, y, matrix, colour_scheme, gradient, fill)


def make_bar(width, x, y, matrix, colour_scheme=None, gradient=None, fill=True):
    return led_matrix_static_objects.Bar(width, x, y, matrix, colour_scheme, gradient, fill)


def make_rect(x1, x2, y1, y2, matrix, colour_scheme=None, gradient=None, fill=True):
    return led_matrix_static_objects.Rect(x1, x2, y1, y2, matrix, colour_scheme, gradient, fill)


def make_line(point_1: tuple, point_2: tuple, matrix, colour_scheme=None, gradient=None, fill=True):
    return led_matrix_static_objects.Line(point_1, point_2, matrix, colour_scheme, gradient, fill)


def make_triangle(p1: tuple, p2: tuple, p3: tuple, matrix, colour_scheme=None, gradient=None, fill=True):
    return led_matrix_static_objects.Triangle(p1, p2, p3, matrix, colour_scheme, gradient, fill)


def set_image(image, matrix, x=0, y=0):
    matrix.SetImage(image, x, y)


# env = PWorld(g=-.5)
#
# for s in range(10):
#     env.add_pixel()
# circle = env.add_circle(pos=Vector2(32, 16), r=3, points=6)
#
# env.simulate_led_matrix()
#
# while True:
#     env.update()




