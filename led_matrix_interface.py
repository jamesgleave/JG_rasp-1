import led_matrix_physics as physics_engine
import led_matrix_physics_objects as physical_objects
from led_matrix_physics import Vector2
import led_matrix_static_objects
import led_matrix_aud_in as JAudio
import numpy as np
import time
from PIL import Image as pimage

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'

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
                  led_size=(64, 32), bounciness=None, gravity_enabled=True): 

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


class Pen:
    """Allows for shapes to be drawn on the matrix
    @:param canvas (rgb matrix) can be left none, if this is done, Pen will create a new matrix object"""

    def __init__(self, canvas):
        if canvas is not None:
            self.matrix = canvas
        else:
            self.matrix = RGBMatrix(options=options)

    def draw_line(self, x1, y1, x2, y2, c):

        if not isinstance(c, graphics.Color):
            c = graphics.Color(c[0], c[1], c[2])

        graphics.DrawLine(self.matrix, x1, y1, x2, y2, c)

    def draw_circle(self, x, y, r, c, fill=False, gradient=None):

        if not isinstance(c, graphics.Color):
            c = graphics.Color(c[0], c[1], c[2])

        if fill:
            for radius in range(r):
                if gradient is not None:
                    red, green, blue = self.__gradient(gradient, x, r, c)
                    c.red, c.green, c.blue = red, green, blue

                graphics.DrawCircle(self.matrix, x, y, radius, c)
        else:
            graphics.DrawCircle(self.matrix, x, y, r, c)

    def draw_text(self, font, x, y, c, text):

        if not isinstance(c, graphics.Color):
            c = graphics.Color(c[0], c[1], c[2])

        graphics.DrawText(self.matrix, font, x, y, c, text)

    def draw_rect(self, x1, y1, x2, y2, c, fill=False, gradient=None):
        if fill:
            for x in range(abs(x2 - x1)):
                if gradient is not None:
                    red, green, blue = self.__gradient(gradient, x, y1, c)
                    c.red, c.green, c.blue = red, green, blue
                self.draw_line(x, y1, x, y2, c)

        else:
            self.draw_line(x1, y1, x2, y1, c)
            self.draw_line(x2, y1, x2, y2, c)
            self.draw_line(x2, y2, x1, y2, c)
            self.draw_line(x1, y2, x1, y1, c)

    def draw_triangle(self, v1, v2, v3, c, fill=False):
        x1, y1 = v1[0], v1[1]
        x2, y2 = v2[0], v2[1]
        x3, y3 = v3[0], v3[1]

        if fill:
            raise Warning("Not Implemented")
            pass
        else:
            self.draw_line(x1, y1, x2, y2, c)
            self.draw_line(x1, y1, x3, y3, c)
            self.draw_line(x2, y2, x3, y3, c)

    @staticmethod
    def __gradient(gradient, x, y, c):
        """This calculates a colour gradient given the value of x and y and adds it to c"""
        r, g, b = c.red, c.green, c.blue

        if 'r_grad_y' in gradient:
            r += 225 * (1 / 32) * y

        if 'g_grad_y' in gradient:
            g += 225 * (1 / 32) * y

        if 'b_grad_y' in gradient:
            b += 225 * (1 / 32) * y

        if 'r_grad_x' in gradient:
            r += 225 * (1 / 64) * x

        if 'g_grad_x' in gradient:
            g += 225 * (1 / 64) * x

        if 'b_grad_x' in gradient:
            b += 225 * (1 / 64) * x

        c = r, g, b = int(r if r < 255 else 255), int(g if g < 255 else 255), int(b if b < 255 else 255)

        if r == 0 and g == 0 and b == 0:
            print(c)
            raise UserWarning("Invalid gradient: " + gradient +
                              ". \nUse one or more of the following:\n" +
                              "r_grad_y, g_grad_y, b_grad_y,\n r_grad_x," +
                              "g_grad_x, b_grad_x.\n" + "The syntax is: " +
                              "(rgb colour value)_grad_(x or y direction)"
                              )

        return c


class Image(physics_engine.PhysicsBody):
    """

    This object allows for image presentation on the matrix. This object inherits all physics aspects from physics
    body to allow for physics to be exacted on images

    """
    def __init__(self, image_path, canvas=None, position=None, environment=None,
                 mass=np.random.randint(1, 10), c=(0, 100, 0), velocity=None,
                 led_size=(64, 32), bounciness=np.random.sample(), gravity_enabled=False, image_size=None):

        super(Image, self).__init__(position=position, environment=environment, mass=mass, matrix=canvas,
                                    c=c, velocity=velocity, led_size=led_size, bounciness=bounciness,
                                    gravity_enabled=gravity_enabled)

        self.image = pimage.open(image_path)

        if image_size is not None:
            self.image_size = image_size
        else:
            self.image_size = (self.m.width, self.m.height)

    def show_image(self):
        # Make image fit our screen.
        self.image.thumbnail(self.image_size, pimage.ANTIALIAS)
        self.m.SetImage(self.image.convert('RGB'))

    def scroll_image(self, speed_x=1, speed_y=0):
        self.image.resize((self.m.width, self.m.height), pimage.ANTIALIAS)

        double_buffer = self.m.CreateFrameCanvas()
        img_width, img_height = self.image.size

        # let's scroll
        xpos = 0
        ypos = 0
        while True:
            xpos += speed_x
            ypos += speed_y
            if xpos > img_width:
                xpos = 0

            if ypos > img_width:
                ypos = 0

            double_buffer.SetImage(self.image, -xpos, -ypos)
            double_buffer.SetImage(self.image, -xpos + img_width, -ypos)

            double_buffer = self.m.SwapOnVSync(double_buffer)
            time.sleep(0.01)

    def check_bounds(self):
        img_width, img_height = self.image.size
        x, y = self.position.x, self.position.y

        if x + img_width > self.m.width or x - img_width < 0:
            self.bounce(1)
        if y + img_height > self.m.height or y - img_height < 0:
            self.bounce(2)

    def update(self):
        self.m.SetImage(self.image, self.position.x, self.position.y)
        self.update_position()
        self.dampen()
        self.check_bounds()
        if self.gravity:
            self.apply_gravity()




def make_circle(r, x, y, matrix, colour_scheme=None, gradient=None, fill=True):
    return led_matrix_static_objects.Circle(r, x, y, matrix, colour_scheme, gradient, fill)


def make_bar(width, x, y, matrix, colour_scheme=None, gradient=None, fill=True):
    return led_matrix_static_objects.Bar(width, x, y, matrix, colour_scheme, gradient, fill)


def make_rect(x1, x2, y1, y2, matrix, colour_scheme=None, gradient=None, fill=True):
    return led_matrix_static_objects.Rect(x1, x2, y1, y2, matrix, colour_scheme, gradient, fill)


def make_line(point_1, point_2, matrix, colour_scheme=None, gradient=None, fill=True):
    return led_matrix_static_objects.Line(point_1, point_2, matrix, colour_scheme, gradient, fill)


def make_triangle(p1, p2, p3, matrix, colour_scheme=None, gradient=None, fill=True):
    return led_matrix_static_objects.Triangle(p1, p2, p3, matrix, colour_scheme, gradient, fill)






