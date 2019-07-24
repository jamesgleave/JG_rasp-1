import numpy as np
import time


class Physics:
    def __init__(self, air_resistance=1.2, g=0):
        self.gravity = g
        self.air_resistance = air_resistance
        self.object_list = []

    def add(self, obj):
        self.object_list.append(obj)

    def update_environment(self):
        for obj in self.object_list:
            obj.update()
            time.sleep(.5)

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
        def print(vector):
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
    def __init__(self, position, environment, matrix=None, c=(100, 0, 0), velocity=Physics.Vector2(0, 0)):
        self.position = position
        self.velocity = velocity
        self.colour = c
        self.environment = environment
        self.m = matrix

        self.update()

    def add_force(self, vel_vector):
        self.velocity.add(vel_vector)

    def update_position(self):
        new_pos_x = self.position.x + self.velocity.x
        new_pos_y = self.position.y + self.velocity.y

        self.position.x = new_pos_x
        self.position.y = new_pos_y

    def update(self):

        print("Position", int(self.position.x), int(self.position.y))
        print("Velocity", (self.velocity.x), (self.velocity.y), "\n")

        self.update_position()
        c = self.colour
        self.dampen()

    def dampen(self):
        f = self.environment.air_resistance
        self.velocity.x = self.velocity.x/f
        self.velocity.y = self.velocity.y/f

        if self.velocity.magnitude() < 0.1:
            self.velocity.make_zero()


env = Physics()
p = PhysicalPixel(Physics.Vector2(0, 0), env)

env.add(p)
env.update_environment()

force = env.create_force_emitter(force=2, radius=4)
force.detonate(env.Vector2(-3, -2))

for _ in range(10):
    env.update_environment()




