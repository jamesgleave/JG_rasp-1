"""

This class creates static shapes (not effected by physics)

"""


class Shape(object):

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


class Rect:
    def __init__(self, width, x, y, matrix, colour_scheme=None, gradient=None):

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


class Circle:
    def __init__(self, r, x, y, matrix, colour_scheme=None, gradient=None):

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


