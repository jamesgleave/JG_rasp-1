import led_matrix_display as display
import numpy as np


class PObject:

    @staticmethod
    def new_pixel(position, environment, mass=np.random.randint(1,10), matrix=None, c=(0, 100, 0), velocity=None,
                  led_size=(64, 32), bounciness=np.random.sample(), gravity_enabled=True):

        return display.PhysicalPixel(position, environment, mass, matrix, c, velocity,
                                     led_size, bounciness, gravity_enabled)

    @staticmethod
    def new_circle(pos, r, points, physical_pixel, fill=False):
        return display.CirclePhysComp(pos, r, points, physical_pixel, fill)


class Environment(display.Physics):

    def __init__(self, air_resistance=0.95, g=-.5, fps=60):
        super().__init__(air_resistance, g, fps)




