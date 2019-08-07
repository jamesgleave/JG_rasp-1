from PIL import Image


class Animation:
    def __init__(self, sprite_list, name):
        self.name = name
        self.sprite_list = sprite_list
        self.animation_index = 0
        self.current_sprite = None

    def animate(self):
        # resets the animation
        if self.animation_index > len(self.sprite_list):
            self.animation_index = 0

        self.current_sprite = self.sprite_list[self.animation_index]
        self.animation_index += 1

    def flip(self):
        for sprite in self.sprite_list:
            sprite = sprite.rotation(180)

    def resize(self, size):
        for sprite in self.sprite_list:
            sprite.thumbnail(size, Image.ANTIALIAS)


class Animator:
    def __init__(self, matrix):
        self.animations = {}
        self.matrix = matrix

    def add_animation(self, *animation):
        # Adds the animations into the dict as {"EXAMPLE_NAME", animation_object}
        for a in animation:
            animation_dict = {a.name: a}
            self.animations.update(animation_dict)

    def animate(self, animation_name):
        return self.animations.get(animation_name).animate