import led_matrix_interface as Jworld
import led_matrix_animator as animator
import time
from led_matrix_interface import Vector2


class Pet(Jworld.physics_engine.PhysicsBody):
    """This class represents the pet itself. This will animate and store all information about the pet.
        The pet eats physical pixels."""

    def __init__(self, position, environment, mass):
        super(Pet, self).__init__(self, position, environment, mass)
        self.brain = {"mood": 1, "hunger": 0, "senses": []}
        self.health = 100

    def mood(self):
        pass

    def move(self, direction_vector):
        pass


class Food(Jworld.physics_engine.PhysicalPixel):

    """The food the Pet eats, the foods energy rating is mapped to the audio input peak strength"""
    def __init__(self, position, environment, mass, energy):
        super(Food, self).__init__(self, position, environment, mass, bounciness=0.1)
        self.name = 'food'
        self.energy = energy


class TimeTracker:
    pass


class GameWorld(Jworld.physics_engine.Physics):
    def __init__(self):
        super(GameWorld, self).__init__(self)

    def create_pet(self):
        pass

    def create_food(self):
        """If audio input threshold exceeds X then create food"""
        pass

    def update_environment(self):
        for obj in self.object_list:
            obj.update()
        frame_sleep = 1 / self.fps
        self.create_food()
        time.sleep(frame_sleep)
