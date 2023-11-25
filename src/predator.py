# import random
# import pygame
from entity import Entity
import time
from pdb import set_trace as bp

# class Predator(Entity):
#     def __init__(self, x, y, size, speed, color, allowed_angle, orientation, entity_type, time_alive, window):
#         super().__init__(x, y, size, speed, color, allowed_angle, orientation, entity_type, window)
#         self.entity_type = 'predator'
#         self.time_alive = time_alive

class Predator(Entity):
    def __init__(self, entity_type='predator',  **kwargs):
        super().__init__(entity_type=entity_type, **kwargs)

    def give_birth(self):
        new_kwargs = self.__dict__.copy()  # Copie des attributs de l'instance actuelle

        _ = new_kwargs.pop('entity_id', None)
        #_ = new_kwargs.pop('reproduction_delay', None)
        new_kwargs['time_alive'] = 0
        new_kwargs['time_since_last_birth'] = 0
        _ = new_kwargs.pop('x_on_grid', None)
        _ = new_kwargs.pop('y_on_grid', None)

        # new_kwargs['window'] = window

        new_predator = Predator(**new_kwargs)

        # new_predator = Predator(x=self.x, y=self.y, size=self.size, speed=self.speed, color=self.color, allowed_angle=self.allowed_angle, orientation=self.orientation, window=window)
        return new_predator
    

