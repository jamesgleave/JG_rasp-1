"""

These classes creates static shapes (not effected by physics)

"""
import numpy as np


class Shape(object):
    def __init__(self, matrix=None, colour_scheme=None, gradient=None):
        self.gradient = gradient
        self.colour = colour_scheme
        self.Dmatrix = matrix

    def build(self):
        pass

    def colorize(self, x, y):

        G = self.gradient
        C = self.colour

        if C is not None:
            r, g, b = C
        else:
            r, g, b = 35, 100, 110

        if G is not None:
            y_lim = self.Dmatrix.options.rows
            x_lim = self.Dmatrix.options.cols

            if 'r_grad_y' in G:
                r = 225 * (1 / y_lim) * y

            if 'g_grad_y' in G:
                g = 225 * (1 / y_lim) * y

            if 'b_grad_y' in G:
                b = 225 * (1 / y_lim) * y

            if 'r_grad_x' in G:
                r = 225 * (1 / x_lim) * x

            if 'g_grad_x' in G:
                g = 225 * (1 / x_lim) * x

            if 'b_grad_x' in G:
                b = 225 * (1 / x_lim) * x

        return r, g, b


class Line(Shape):
    def __init__(self, point_1: tuple, point_2: tuple, matrix, colour_scheme=None, gradient=None, fill=True):
        super(Line, self).__init__()

        """Summary of Construction

                Parameters:
                width (int): width of the Rect object
                point_1 (tuple): tuple of the starting point (x, y)
                point_2 (tuple): tuple of the starting point (x, y)
                matrix (RGBMatrix): the matrix object this shape will be drawn on
                colour_scheme (Tuple): (r, g, b) values of the Rect
                gradient (String): The gradient is an stylistic option. Depending on what is passed,
                the rect object will have a color gradient. The options are:
                - 'r_grad_y' : increases the r value as y increases
                - 'g_grad_y' : increases the g value as y increases
                - 'b_grad_y' : increases the b value as y increases

                - 'r_grad_x' : increases the r value as x increases
                - 'g_grad_x' : increases the g value as x increases
                - 'b_grad_x' : increases the b value as x increases

                These can be combined with a - in the middle. For example:
                - 'r_grad_y-g_grad_x''

               """

        self.x1 = point_1[0]
        self.x2 = point_2[0]
        self.y1 = point_1[1]
        self.y2 = point_2[1]

        self.Dmatrix = matrix
        self.colour = colour_scheme
        self.gradient = gradient

    def build(self):
        x1 = np.min(self.x1, self.x2)
        y1 = np.min(self.y1, self.y2)

        x2 = np.min(self.x1, self.x2)
        y2 = np.min(self.y1, self.y2)

        dx = x2 - x1
        dy = y2 - y1
        for x in range(x1, x2):
            y = y1 + dy * (x - x1) / dx
            r, g, b = self.colorize(x, y)

            self.Dmatrix.SetPixel(x, y, r, g, b)


class Circle(Shape):
    def __init__(self, r, x, y, matrix, colour_scheme=None, gradient=None, fill=True):
        super(Circle, self).__init__()

        """Summary of Construction

        Parameters:
        r (int): radius of the circle object
        x (int): x position of the bar
        y (int): y position of the bar
        matrix (RGBMatrix): the matrix object this shape will be drawn on
        colour_scheme (Tuple): (r, g, b) values of the Rect
        gradient (String): The gradient is an stylistic option. Depending on what is passed,
        the rect object will have a color gradient. The options are:
        - 'r_grad_y' : increases the r value as y increases
        - 'g_grad_y' : increases the g value as y increases
        - 'b_grad_y' : increases the b value as y increases

        - 'r_grad_x' : increases the r value as x increases
        - 'g_grad_x' : increases the g value as x increases
        - 'b_grad_x' : increases the b value as x increases

        These can be combined with a - in the middle. For example:
        - 'r_grad_y-g_grad_x''

       """

        self.r = r
        self.x = x
        self.y = y
        self.Dmatrix = matrix
        self.colour = colour_scheme
        self.gradient = gradient

        self.build()

    def build(self):
        for x in range(self.x):
            for y in range(self.y):
                x_squared = x * x
                r_squared = self.r * self.r
                y = np.sqrt(r_squared - x_squared)

                r, g, b = self.colorize(x, y)
                self.Dmatrix.SetPixel(x + self.x, y + self.y, r, g, b)
                self.Dmatrix.SetPixel(x + self.x, -y + self.y, r, g, b)


class Rect(Shape):
    def __init__(self, width, x, y, matrix, colour_scheme=None, gradient=None, fill=True):
        super(Rect, self).__init__()

        """Summary of Construction

        Parameters:
        width (int): width of the Rect object
        x (int): x position of the bar
        y (int): y position of the bar
        matrix (RGBMatrix): the matrix object this shape will be drawn on
        colour_scheme (Tuple): (r, g, b) values of the Rect
        gradient (String): The gradient is an stylistic option. Depending on what is passed,
        the rect object will have a color gradient. The options are:
        - 'r_grad_y' : increases the r value as y increases
        - 'g_grad_y' : increases the g value as y increases
        - 'b_grad_y' : increases the b value as y increases

        - 'r_grad_x' : increases the r value as x increases
        - 'g_grad_x' : increases the g value as x increases
        - 'b_grad_x' : increases the b value as x increases

        These can be combined with a - in the middle. For example:
        - 'r_grad_y-g_grad_x''

       """

        self.w = width
        self.x = x
        self.y = y
        self.Dmatrix = matrix
        self.colour = colour_scheme
        self.gradient = gradient

        self.build()

    def build(self):
        """Builds the Rect onscreen."""
        for x_bar in range(self.w):
            for y_bar in range(self.y):
                r, g, b = self.colorize(x=x_bar, y=y_bar)
                self.Dmatrix.SetPixel(x_bar + self.x, y_bar, r, g, b)

    def hollow_build(self):
        """Builds the hollow Rect onscreen."""
        for x_bar in range(self.w):
            for y_bar in range(self.y):
                r, g, b = self.colorize(x=x_bar, y=y_bar)
                if x_bar == 0 or x_bar == self.w - 1:
                    self.Dmatrix.SetPixel(x_bar + self.x, y_bar, r, g, b)
                else:
                    self.Dmatrix.SetPixel(x_bar + self.x, 0, r, g, b)
                    self.Dmatrix.SetPixel(x_bar + self.x, self.y, r, g, b)


class Triangle(Shape):
    def __init__(self, p1, p2, p3, matrix, colour_scheme=None, gradient=None, fill=True):
        super(Triangle, self).__init__()
        self.p1, self.p2, self.p3 = p1, p2, p3

        self.Dmatrix = matrix
        self.colour = colour_scheme
        self.gradient = gradient
        self.build()

    def build(self):
        x1, x2, x3 = self.p1[0], self.p1[0], self.p3[0]
        y1, y2, y3 = self.p1[0], self.p1[0], self.p3[0]

        Line((x1, y1), (x2, y2), matrix=self.Dmatrix, colour_scheme=self.colour, gradient=self.gradient)
        Line((x1, y1), (x3, y3), matrix=self.Dmatrix, colour_scheme=self.colour, gradient=self.gradient)
        Line((x2, y2), (x3, y3), matrix=self.Dmatrix, colour_scheme=self.colour, gradient=self.gradient)










