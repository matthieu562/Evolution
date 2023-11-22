from entity import Entity
import random
import time
from constants import *

class Food(Entity):
    def __init__(self, entity_type='food', **kwargs):
        super().__init__(entity_type=entity_type,  **kwargs)

    def give_birth(self):
        # new_kwargs = self.__dict__.copy()  # Copie des attributs de l'instance actuelle
        # _ = new_kwargs.pop('reproduction_delay', None)

        # WINDOW_WIDTH, WINDOW_HEIGHT = window.get_size()
        new_prey = Food(
                        # window,
                        x=self.x,
                        y=self.y,
                        size=random.randint(FOOD_MIN_SIZE, FOOD_MAX_SIZE),
                        speed=0,
                        color=(0, random.randint(FOOD_MIN_COLOR, FOOD_MAX_COLOR), 0),
                        # allowed_angle=0,
                        # orientation=0,
                        time_since_last_birth=0,
                        reproduction_delay=random.randint(MIN_REPRODUCTION_DELAY, MAX_REPRODUCTION_DELAY)
                    )
        return new_prey