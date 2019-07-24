import numpy as np
import time

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    print("The package rgbmatrix was not found")


class Physics:
    def __init__(self, air_resistance=0.991, g=0, fps=60):
        self.gravity = g
        self.air_resistance = air_resistance
        self.object_list = []
        self.fps = fps

    def add(self, obj):
        self.object_list.append(obj)

    def update_environment(self):
        for obj in self.object_list:
            obj.update()
        frame_sleep = 1 / self.fps
        time.sleep(frame_sleep)

    def create_force_emitter(self, force, radius):
        return self.ForceEmitter(force, radius, self.object_list)

    def get_object_list(self):
        return self.object_list

    def get_object_count(self):
        return len(self.object_list)

    class Vector2():
        def __init__(self, x, y):
            self.vector = [x, y]
            self.x = self.vector[0]
            self.y = self.vector[1]

        def add(self, other_vector):
            self.x = self.x + other_vector.x
            self.y = self.y + other_vector.y

        def negate(self, other_vector):
            self.x = self.x - other_vector.x
            self.y = self.y - other_vector.y

        def scalar_mult(self, val):
            self.x *= val
            self.y *= val

        def make_zero(self):
            self.x, self.y = 0, 0

        def dist_from(self, other_vector):
            x_sum = self.x - other_vector.x
            y_sum = self.y - other_vector.y

            return np.sqrt(np.square(x_sum) + np.square(y_sum))

        def magnitude(self):
            squared_sum = np.square(self.x) + np.square(self.y)
            return np.sqrt(squared_sum)

        def normalize(self):
            magnitude = self.magnitude()
            unit_vector = Physics.Vector2.scale(self, magnitude)
            return unit_vector

        def get_position(self):
            pos = (int(self.x), int(self.y))
            return pos

        @staticmethod
        def relative_direction(origin_vector, other_vector):
            origin_vector.negate(other_vector)
            return origin_vector

        @staticmethod
        def mult(u, v):
            return Physics.Vector2(u.x * v.x, u.y * v.y)

        @staticmethod
        def scale(vect, val):
            return Physics.Vector2(vect.x * val, vect.y * val)

        @staticmethod
        def print_vector(vector):
            print("<" + str(vector.x) + ",", str(vector.y) + ">")

    class ForceEmitter:
        def __init__(self, force, radius, obj_list):
            self.force = force
            self.radius = radius
            self.obj_list = obj_list

        def detonate(self, position, force=None):

            if force is None:
                force = self.force

            for obj in self.obj_list:
                if position.dist_from(obj.position) < self.radius:
                    force_direction = Physics.Vector2.relative_direction(position, obj.position)

                    force_direction.scalar_mult(force)
                    obj.add_force(force_direction)


class PhysicalPixel:
    def __init__(self, position, mass, environment, matrix, c=(0, 100, 0), velocity=Physics.Vector2(0, 0), led_size=(32,64)):
        self.position = position
        self.velocity = velocity
        self.mass = mass * 1000

        self.colour = c
        self.environment = environment
        self.m = matrix
        self.led_size = led_size

        self.update()

    def add_force(self, f):
        self.velocity.add(Physics.Vector2.scale(f, (1/self.mass)))

    def update_position(self):
        new_pos_x = self.position.x + self.velocity.x
        new_pos_y = self.position.y + self.velocity.y

        self.position.x = new_pos_x
        self.position.y = new_pos_y

    def update(self):

        if self.m is not None:
            self.m.SetPixel(self.position.x, self.position.y,
                            self.colour[0], self.colour[1],
                            self.colour[2])

        self.update_position()
        self.dampen()
        self.check_bounds()
    
    def check_bounds(self):
        if self.position.x > self.led_size[0] or self.position.x < 0:
            self.delete()
        if self.position.y > self.led_size[1] or self.position.y < 0:
            self.delete()
            
    def delete(self):
        del self

    def dampen(self):
        f = self.environment.air_resistance
        self.velocity.x = self.velocity.x * f
        self.velocity.y = self.velocity.y * f

        if self.velocity.magnitude() < 0.001:
            self.velocity.make_zero()






