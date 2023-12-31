from entity import Entity
import time
from pdb import set_trace as bp


class Prey(Entity):
    def __init__(self, entity_type='prey', **kwargs):
        super().__init__(entity_type=entity_type, **kwargs)
    
    def give_birth(self):
        new_kwargs = self.__dict__.copy()  # Copie des attributs de l'instance actuelle

        #_ = new_kwargs.pop('reproduction_delay', None)
        _ = new_kwargs.pop('entity_id', None)
        _ = new_kwargs.pop('x_on_grid', None)
        _ = new_kwargs.pop('y_on_grid', None)
        new_kwargs['time_alive'] = 0
        new_kwargs['time_since_last_birth'] = 0
        # new_kwargs['window'] = window

        new_prey = Prey(**new_kwargs)
        return new_prey
