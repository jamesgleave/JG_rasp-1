import numpy as np
import time

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    print("The package rgbmatrix was not found")


class Physics:
    def __init__(self, air_resistance=0.95, g=-.5, fps=60):
        self.gravity = g
        self.air_resistance = air_resistance
        self.object_list = []
        self.fps = fps

    def add(self, obj):
        self.object_list.append(obj)

    def add_list(self, obj_list):
        for o in obj_list:
            self.object_list.append(o)

    def add_physical_body(self, obj):
        self.add_list(obj.point_list)

    def update_environment(self):
        for obj in self.object_list:
            obj.update()
        frame_sleep = 1 / self.fps
        time.sleep(frame_sleep)

    def get_object_list(self):
        return self.object_list

    def clear(self):
        self.object_list.clear()

    def get_object_count(self):
        return len(self.object_list)

    def print_all_current_object_positions(self):
        for obj in self.object_list:
            Vector2.print_vector(obj.position)

    @staticmethod
    def occupies_same_space(coordinate1, coordinate2):
        return coordinate1[0] == coordinate2[0] and coordinate1[1] == coordinate2[1]


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other_vector):
        self.x += other_vector.x
        self.y += other_vector.y

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
        unit_vector = Vector2.scale(self, 1/magnitude)
        return unit_vector

    def get_position(self):
        pos = (int(self.x), int(self.y))
        return pos

    @staticmethod
    def relative_direction(origin_vector, other_vector):
        o_v = Vector2(origin_vector.x, origin_vector.y)
        o_v.negate(other_vector)
        return o_v

    @staticmethod
    def mult(u, v):
        return Vector2(u.x * v.x, u.y * v.y)

    @staticmethod
    def scale(vect, val):
        return Vector2(vect.x * val, vect.y * val)

    @staticmethod
    def dot(vect1, vect2):
        return vect1.x * vect2.x + vect1.y * vect2.y

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
                force_direction = Vector2.relative_direction(position, obj.position)
                force_direction.scalar_mult(force)

                obj.add_force(force_direction)


class PhysicalPixel:
    def __init__(self, position, environment, mass=np.random.randint(1,10), matrix=None, c=(0, 100, 0), velocity=None,
                 led_size=(64, 32), bounciness=np.random.sample(), gravity_enabled=True):

        self.position = position
        self.mass = mass * 1000

        if velocity is None:
            velocity = Vector2(0, 0)
        self.velocity = velocity

        self.momentum = None
        self.bounciness = bounciness

        self.colour = c
        self.environment = environment
        self.m = matrix
        self.led_size = led_size
        self.gravity = gravity_enabled

        self.update()

    def add_force(self, f):
        self.velocity.add(Vector2.scale(f, (1/self.mass)))

    def update_position(self):
        new_pos_x = self.position.x + self.velocity.x
        new_pos_y = self.position.y + self.velocity.y

        if new_pos_x > self.led_size[0] or new_pos_x < 0:
            """Do nothing"""
            self.bounce(1)

        else:
            self.position.x = new_pos_x

        if new_pos_y > self.led_size[1] or new_pos_y < 0:
            """Do nothing"""
            self.bounce(2)
        else:
            self.position.y = new_pos_y

        # self.position.x = new_pos_x
        # self.position.y = new_pos_y

    def update(self):

        if self.m is not None:
            self.m.SetPixel(self.position.x, self.position.y,
                            self.colour[0], self.colour[1],
                            self.colour[2])

        self.update_position()
        self.dampen()
        self.check_bounds()

        if self.gravity:
            self.apply_gravity()
    
    def check_bounds(self):
        if self.position.x >= self.led_size[0] or self.position.x <= 0:
            self.bounce(1)

        if self.position.y >= self.led_size[1] or self.position.y <= 0:
            self.bounce(2)
            
    def bounce(self, i):
        # V new = b * ( -2*(V dot N)*N + V )

        # V new = self.bounciness * ( -2 * N * (self.velocity dot N) + self.velocity )

        # R = 2*(V dot N) * N - V
        # dot = Vector2.dot(self.velocity, self.velocity.normalize())
        # dot *= 2
        # prod = Vector2.scale(self.velocity.normalize(), dot)
        #
        # prod.negate(self.velocity)
        #
        # self.velocity = prod

        if i == 1:
            self.velocity.x *= -1
            self.velocity.scalar_mult(self.bounciness + (self.mass/50000))
        else:
            self.velocity.y *= -1
            self.velocity.scalar_mult(self.bounciness + (self.mass/50000))

    def dampen(self):
        f = self.environment.air_resistance

        self.momentum = Vector2.scale(self.velocity, self.mass)

        self.velocity.x = self.velocity.x * f
        self.velocity.y = self.velocity.y * f

    def apply_gravity(self):
        self.velocity.y -= self.environment.gravity

    def clone(self):
        x = self.position.x
        y = self.position.y

        mass = self.mass/1000
        env = self.environment
        matrix = self.m

        return PhysicalPixel(position=Vector2(x, y), mass=mass,
                             environment=env, matrix=matrix)






