import led_matrix_interface as Jworld
import random
from led_matrix_util import clamp
from led_matrix_interface import Vector2 as Vector


class Tree:
    def __init__(self):
        self.tree = []
        self.tree.append(Walker(Vector(32, 16)))
        self.pen = Jworld.Pen(canvas=None)

    def show_tree(self):
        for i in self.tree:
            if i.radius != 1:
                self.pen.draw_circle(x=i.position.x, y=i.position.y, r=i.radius,
                                     c=(100, 50, i.position.dist_from(Vector(32, 16))))
            else:
                self.pen.matrix.SetPixel(x=i.position.x, y=i.position.y, r=i.radius,
                                         c=(100, 50, i.position.dist_from(Vector(32, 16))))

    def check_for_stuck(self, walker):
        for i in self.tree:
            if walker.position.dist_from(i.position) > 2 * i.radius:
                i.stuck = True
                self.tree.append(i)


class Walker:
    def __init__(self, position=None):

        if position is None:
            self.position = Vector.random_vector()

        self.velocity = Vector.random_vector().make_zero()
        self.radius = 4
        self.stuck = False

    def walk(self):
        if not self.stuck:
            self.velocity = Vector(random.sample() * self.radius, random.sample() * self.radius)
            self.position.add(self.velocity)
            self.position.x = clamp(self.position.x, 0, 64)
            self.position.y = clamp(self.position.y, 0, 32)


