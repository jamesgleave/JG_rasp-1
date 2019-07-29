import led_matrix_physics_objects as display
from led_matrix_physics_objects import Vector2
import numpy as np


class PWorld:

    def __init__(self, air_resistance=0.95, g=.5, fps=60):
        self.environment = display.Physics(air_resistance=air_resistance, g=g, fps=fps)
        self.simulated_matrix = None

    def add_pixel(self, environment=None, position=None,
                  mass=None, matrix=None, c=None, velocity=None,
                  led_size=(64, 32), bounciness=None, gravity_enabled=True) -> display.PhysicalPixel:

        if environment is None:
            environment = self.environment

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

        return self.environment.add(display.PhysicalPixel(position, environment, mass, matrix, c, velocity,
                                    led_size, bounciness, gravity_enabled))

    def add_circle(self, pos, r, points, environment=None,
                   mass=None, matrix=None, c=None, led_size=(64, 32),
                   bounciness=None, gravity_enabled=True, fill=False):

        if environment is None:
            environment = self.environment

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

        physical_pixel = display.PhysicalPixel(environment=environment, mass=mass, matrix=matrix, c=c,
                                               led_size=led_size, bounciness=bounciness,
                                               gravity_enabled=gravity_enabled, position=Vector2.random_vector())

        return self.environment.add_physical_body(display.CirclePhysComp(pos, r, points, physical_pixel, fill))

    def update(self):
        self.environment.update_environment()

        if self.simulated_matrix is not None:
            self.simulated_matrix.simulate_led_matrix()

    def simulate_led_matrix(self):
        self.simulated_matrix = display.MatrixSimulator(self.environment.object_list)

    def empty(self):
        self.environment.clear()

    def print_all_physical_object_positions(self):
        for i in self.environment.get_object_list():
            Vector2.print_vector(i.position)


env = PWorld(g=-.5)

for s in range(10):
    env.add_pixel()
circle = env.add_circle(pos=Vector2(32, 16), r=3, points=6)

env.simulate_led_matrix()

while True:
    env.update()
    env.print_all_physical_object_positions()




