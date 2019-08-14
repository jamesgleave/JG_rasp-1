import datetime
import time
import math

class Time:
    def __init__(self):
        # launch_time is the time the Time object was initialized
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.formatted_time = None
        self.seconds_since_instantiation = 0

    def get_time(self):
        self.hour = str(datetime.datetime.now().time().hour)
        self.minute = str(datetime.datetime.now().time().minute)
        self.second = str(datetime.datetime.now().time().second)

        self.seconds_since_instantiation = self.seconds_since_instantiation + 1
        if self.seconds_since_instantiation >= 86400:
            self.seconds_since_instantiation = 0

        self.formatted_time = self.hour+":"+self.minute+":"+self.second
        return datetime.datetime.now().ctime()[11:20],\
               datetime.datetime.now().ctime()[:11], \
               datetime.datetime.now().ctime()[20:]

    @staticmethod
    def sleep_second():
        time.sleep(1)

    def test(self, h):
        if h > 23:
            h = 0
        h += 1
        time.sleep(.1)
        self.seconds_since_instantiation += 1
        return h


class SevenSegmentCharacter:
    def __init__(self, size):
        assert size % 2 == 0


class Clock(Time):
    def __init__(self, display_type=None, matrix=None):
        super(Clock, self).__init__()
        self.display = display_type
        self.matrix = matrix
        # self.max_brightness = self.matrix.brightness
        self.max_brightness = 100
        self.brightness = 255

    def classic(self, brightness, colour, font_path="../../../fonts/7x13.bdf"):
        """
        This is a classic digital clock

        brightness - the intensity of each led.
        colour - the colour of the clock
        font - the font of the clock
        """

        font = graphics.Font()
        font.LoadFont(font_path)
        textColor = graphics.Color(colour[0], colour[1], colour[2])
        pos = 0
        my_text = self.get_time()[0]

        self.brightness = brightness
        self.matrix.brightness = self.brightness

        while True:
            self.matrix.Clear()
            graphics.DrawText(self.matrix, font, pos, 10, textColor, my_text)
            my_text = self.get_time()
            self.sleep_second()

    def classic_smartclock(self, brightness, colour, font_path="../../../fonts/7x13.bdf"):
        """
        This is a smart digital clock which lowers its
        brightness depending on the hour

        brightness - the initial intensity of each led.
        colour - the colour of the clock
        font - the font of the clock
        """
        font = graphics.Font()
        font.LoadFont(font_path)
        textColor = graphics.Color(colour[0], colour[1], colour[2])
        pos = 0
        my_text = self.get_time()[0]
        self.brightness = 255

        while True:
            self.matrix.Clear()
            graphics.DrawText(self.matrix, font, pos, 10, textColor, my_text)
            my_text = self.get_time()
            self.sleep_second()

            if self.seconds_since_instantiation % 60 == 0:
                self.calculate_brightness()
                self.matrix.brightness = self.brightness

        pass

    def classic_colourshift(self, brightness, colour, font_path="../../../fonts/7x13.bdf"):
        """
        This is a digital clock which shifts its
        colour depending on the hour

        brightness - the intensity of each led.
        colour - the initial colour of the clock
        font - the font of the clock
        """
        pass

    def classic_smart_colourshift(self, brightness, colour, font_path="../../../fonts/7x13.bdf"):
        """
        This is a smart digital clock which shifts its
        colour and brightness depending on the hour

        brightness - the initial intensity of each led.
        colour - the initial colour of the clock
        font - the font of the clock
        """
        pass

    def time_colour_mapping(self, colour):
        minutes_since_instantiation = self.seconds_since_instantiation % 60
        min_per_day = 1440

    def calculate_brightness(self):
        # TODO make a circle function for this that is low between 11 and 8:00
        hour = int(self.hour)
        if hour > 0:
            brightness_scalar = 0.99
            self.brightness *= brightness_scalar
        if hour < 8:
            brightness_scalar = 1.11
            self.brightness *= brightness_scalar

        # clamp(brightness_scalar, 10, self.max_brightness)
        return self.brightness, self.hour

t = Clock()
print(t.get_time())
h = 0
for i in range(720):
    print(t.calculate_brightness())
    t.get_time()
    t.time_colour_mapping((100, 0, 200))
    if t.seconds_since_instantiation == 0:
        break
