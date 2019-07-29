"""

This class creates static shapes (not effected by physics)

"""


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

        self.build()

    def build(self):
        r, g, b = 0, 0, 100

        for x_bar in range(self.w):
            for y_bar in range(self.y):

                r = self.y
                g = x_bar

                self.Dmatrix.SetPixel(x_bar + self.x, y_bar, r, g, b)