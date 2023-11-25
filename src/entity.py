import math
import pygame
import random
from pygame.surface import Surface
from typing import Tuple
from pdb import set_trace as bp
import time
from timeMeasure import TimeMeasure
from constants import *
from utils import *

class Entity:
    all_entities = []
    entity_id = 0
    time_measure = TimeMeasure()
    grid_content = {}
    
    def __init__(self, 
                    # window,
                    x,
                    y,
                    size,
                    speed,
                    entity_type,
                    reproduction_delay,
                    color,
                    allowed_angle=0,
                    orientation=0,
                    vision_angle=0,
                    vision_range=0,
                    time_alive=0,
                    time_since_last_orient_change=0, 
                    time_since_last_birth=0,
                    detected_entities=[]
                 ):
        self.entity_type = entity_type

        if self.is_food() and len(Entity.get_all_foods()) >= FOOD_MAX_UNITS:
            return None
            
        self.size = size
        # window_width, window_height = window.get_size()
        # x=random.randint(0, window_width),
        # y=random.randint(0, window_height),
        adjusted_coords = self.adjust_new_spawn_coords(x, y)
        if adjusted_coords:
            self.x, self.y = adjusted_coords
        else:
            return None
        self.allowed_angle = allowed_angle
        self.orientation = orientation
        self.speed = speed
        self.color = color
        self.reproduction_delay = reproduction_delay #reproduction_delay=random.randint(MIN_REPRODUCTION_DELAY, MAX_REPRODUCTION_DELAY)
        self.time_since_last_birth = time_since_last_birth
        self.time_alive = time_alive
        self.time_since_last_orient_change = time_since_last_orient_change
        self.vision_angle = vision_angle
        self.vision_range = vision_range
        self.detected_entities = detected_entities
        self.x_on_grid, self.y_on_grid = get_new_xy_on_grid(self.x, self.y)

        self.update_grid_content()

        self.entity_id = Entity.entity_id
        Entity.entity_id += 1
        Entity.all_entities.append(self)

    def move(self):
        old_x = self.x
        old_y = self.y

        #self.detect_entities(entities)

        ## Give random orientation and speed
        radian_angle = math.radians(self.orientation)  # Conversion en radians
        magnitude = random.uniform(0, 1)

        self.x = self.x + self.speed * magnitude * math.cos(radian_angle)
        self.y = self.y + self.speed * magnitude * math.sin(radian_angle)
        if self.time_since_last_orient_change >= ORIENT_CHANGE_DELAY:
            _, self.orientation = divmod(self.orientation + random.randint(-self.allowed_angle, self.allowed_angle), 360)
            self.time_since_last_orient_change = 0

        ## Take action
        collided_entity_and_dist = self.collide_with_filtered()
        if collided_entity_and_dist:
            collided_entity, _ = collided_entity_and_dist
            collided_entity_old_x = collided_entity.x
            collided_entity_old_y = collided_entity.y
            if self.is_predator() and collided_entity.is_prey():
                #self.size += 1
                # WARNING if 'collided_entity' is 'self' might be bugged with '__del__'
                collided_entity.killed()
                self.give_birth()
            elif self.is_prey() and collided_entity.is_food():
                #self.size += 1
                collided_entity.killed()
                self.give_birth()
            # else:
            #     pass
                #self.push(collided_entity, distance)
                

        ## Check for collision 
        if self.is_window_collision() or collided_entity_and_dist: #or collided_entity
            self.x = old_x
            self.y = old_y

        ## Update grid
        has_grid_changed = self.update_xy_on_grid()
        if has_grid_changed:
            self.update_grid_content(old_x, old_y)

    def push(self, collided_entity, distance):
        # distance_pushed = self.size + collided_entity.size - distance / 2
        # collision_orient = 
        
        # Calcul du vecteur de direction entre les deux entités
        direction_x = collided_entity.x - self.x
        direction_y = collided_entity.y - self.y

        # S'assurer qu'il n'y a pas de division par zéro
        # if distance == 0:
        #     distance = 1

        # Normalisation du vecteur de direction
        direction_x /= distance
        direction_y /= distance

        # Calcul d'une distance pour les repousser
        repel_distance = (self.size + collided_entity.size - distance) / 2

        # Mise à jour des positions pour les repousser
        self.x -= direction_x * repel_distance
        self.y -= direction_y * repel_distance
        collided_entity.x += direction_x * repel_distance
        collided_entity.y += direction_y * repel_distance

    def update_grid_content(self, old_x=None, old_y=None):
        if old_x and old_y:
            self.remove_grid_content(old_x, old_y)
            # old_x_on_grid, old_y_on_grid = get_new_xy_on_grid(old_x, old_y)
            # old_key = get_key(old_x_on_grid, old_y_on_grid)
            # try:
            #     if len(Entity.grid_content[old_key]) == 1:
            #         del Entity.grid_content[old_key]
            #     elif len(Entity.grid_content[old_key]) > 1:
            #         # del Entity.grid_content[old_key][0]
            #         Entity.grid_content[old_key].remove(self)
            # except KeyError:
            #     bp()
                # Entity.grid_content[old_key].remove(self)
        key = get_key(self.x_on_grid, self.y_on_grid)
        # Si la clé existe déjà
        if key in Entity.grid_content:
            # Si la valeur n'est pas une liste, la convertir en liste
            # if not isinstance(Entity.grid_content[key], list):
            #     self.grid_content[key] = [Entity.grid_content[key]]
            # Ajouter la nouvelle valeur à la liste existante
            Entity.grid_content[key].append(self)
        else:
            # Si la clé n'existe pas, ajouter la nouvelle clé et sa valeur
            Entity.grid_content[key] = [self]

    def remove_grid_content(self, old_x=None, old_y=None):
        x = old_x if old_x else self.x
        y = old_y if old_y else self.y
        x_on_grid, y_on_grid = get_new_xy_on_grid(x, y)
        key = get_key(x_on_grid, y_on_grid) 
        try:
            if len(Entity.grid_content[key]) == 1:
                del Entity.grid_content[key]
            elif len(Entity.grid_content[key]) > 1:
                # del Entity.grid_content[key][0]
                Entity.grid_content[key].remove(self)
        except (KeyError, ValueError) as err:
            bp()

    def update_xy_on_grid(self):
        new_x_on_grid, new_y_on_grid = get_new_xy_on_grid(self.x, self.y)
        if self.x_on_grid != new_x_on_grid or self.y_on_grid != new_y_on_grid:
            self.x_on_grid = new_x_on_grid
            self.y_on_grid = new_y_on_grid
            return True
        return False
        
    def update_status(self):
        if self.is_predator() and self.time_alive >= PREDATORS_LIVETIME:
            self.killed()
        if self.is_prey() and self.time_alive >= PREYS_LIVETIME:
            self.killed()
        if self.is_food() and self.time_since_last_birth >= self.reproduction_delay:
            self.give_birth()
            self.time_since_last_birth = 0
    
    def update_time_properties(self):
        self.time_since_last_birth += 1
        self.time_alive += 1
        self.time_since_last_orient_change += 1

    def killed(self):
        self.remove_grid_content()
        # del self
        try:
            Entity.all_entities.remove(self)
        except ValueError:
            pass

    def is_window_collision(self):
        right = self.x < 0 + self.size
        left = self.x + self.size > WINDOW_WIDTH
        up = self.y < 0 + self.size
        down = self.y + self.size > WINDOW_HEIGHT
        if right or left or up or down:
            return True
        return False

    # def is_window_collision(self):
    #     right = self.x < 0 + self.size
    #     left = self.x + self.size > WINDOW_WIDTH
    #     up = self.y < 0 + self.size
    #     down = self.y + self.size > WINDOW_HEIGHT
    #     if right or left or up or down:
    #         return right, left, up, down
    #     return None, None, None, None
    
    def collide_with_filtered(self):
        new_x_on_grid, new_y_on_grid = get_new_xy_on_grid(self.x, self.y)
        keys = get_keys(new_x_on_grid, new_y_on_grid)
        potential_entities = [] 
        for key in keys:
            if key in Entity.grid_content:
                potential_entities.extend(Entity.grid_content[key])
        return self.collide_with(potential_entities)
    
    def collide_with(self, entities):
        for other_entity in entities:
            if other_entity != self:
                # x Filter
                x_max_lim = self.x + (self.size + other_entity.size)
                x_min_lim = self.x - (self.size + other_entity.size)
                if other_entity.x < x_min_lim or other_entity.x > x_max_lim:
                    continue
                # y Filter
                y_max_lim = self.y + (self.size + other_entity.size)
                y_min_lim = self.y - (self.size + other_entity.size)
                if other_entity.y < y_min_lim or other_entity.y > y_max_lim:
                    continue
                distance = ((self.x - other_entity.x) ** 2 + (self.y - other_entity.y) ** 2) ** 0.5
                if distance <= (self.size + other_entity.size): 
                    return other_entity, distance
        return None

    def detect_entities(self, entities):
        current_detected_entities = []
        for other_entity in entities:
            if other_entity != self:
                # x Filter
                x_max_lim = self.x + (self.vision_range + other_entity.size)
                x_min_lim = self.x - (self.vision_range + other_entity.size)
                if other_entity.x < x_min_lim or other_entity.x > x_max_lim:
                    continue
                # y Filter
                y_max_lim = self.y + (self.vision_range + other_entity.size)
                y_min_lim = self.y - (self.vision_range + other_entity.size)
                if other_entity.y < y_min_lim or other_entity.y > y_max_lim:
                    continue
                # Calcul de l'angle entre l'entité et l'autre entité
                angle_to_entity = math.atan2(other_entity.y - self.y, other_entity.x - self.x)
                angle_difference = (angle_to_entity - math.radians(self.orientation)) % (2 * math.pi)
                # Vérification si l'entité est dans le champ de vision
                if angle_difference < math.radians(self.vision_angle / 2) and angle_difference > -math.radians(self.vision_angle / 2):
                    distance = math.sqrt((self.x - other_entity.x) ** 2 + (self.y - other_entity.y) ** 2)
                    if distance <= self.vision_range:
                        current_detected_entities.append(other_entity)
        self.detected_entities = current_detected_entities

    def is_prey(self):
        return self.entity_type == 'prey'

    def is_predator(self):
        return self.entity_type == 'predator'
    
    def is_food(self):
        return self.entity_type == 'food'
    
    def __del__(self):
        # Code executé avant d'etre supprimé ici, askip del est appelé a un moment random ...
        pass

    def is_inside_window(self):
        return 0 <= self.x <= WINDOW_WIDTH and 0 <= self.y <= WINDOW_HEIGHT

    def adjust_new_spawn_coords(self, x: float, y: float) -> Tuple[float, float]:
        radius = self.size
        radius_step = 3
        angle = random.randint(0, 359) # Angle initial
        angle_step = 30 # En degrés 
        self.x = x
        self.y = y
        # un tour complet est fait en 180/angle_step incrementations (si angle_step alors incrementations = 6)
        
        increment = 0
        nb_time_is_outside = 0
        while self.collide_with_filtered() or self.is_window_collision():
            quotient, _ = divmod(angle + angle_step * increment, 180)
            added_x = (radius + radius_step * quotient) * math.cos(angle + angle_step * increment)
            added_y = (radius + radius_step * quotient) * math.sin(angle + angle_step * increment)

            self.x = self.x + added_x
            self.y = self.y + added_y
            
            if not self.is_inside_window():
                nb_time_is_outside += 1
                if nb_time_is_outside > 6:
                    return None
            else:
                nb_time_is_outside = 0
            increment += 1
        return self.x, self.y
    
    @classmethod
    def get_all_entities(cls):
        return cls.all_entities
    
    @classmethod
    def get_all_preys(cls):
        return [entity for entity in cls.all_entities if entity.entity_type == 'prey']

    @classmethod
    def get_all_predators(cls):
        return [entity for entity in cls.all_entities if entity.entity_type == 'predator']
    
    @classmethod
    def get_all_foods(cls):
        return [entity for entity in cls.all_entities if entity.entity_type == 'food']

    def __str__(self):
        return (f"""\t{self.entity_type} id: {self.entity_id}\
              \n\t({self.x}, {self.y})\
              \n\tsize: {self.size}\
              \n\tspeed: {self.speed}\
              \n\tcolor: {self.color}\
              \n\tallowed_angle: {self.allowed_angle}\
              \n\torientation: {self.orientation}\
              \n\tdetected_entities: {[id.entity_id for id in self.detected_entities]}\
              \n\tEntity count: {len(Entity.get_all_entities())}\
              """)

    def draw(self, window):
        #self.display_vision(window)
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)
        #self.draw_id(window)

    def draw_id(self, window):
        font = pygame.font.Font(None, 20)
        text_surface = font.render(str(self.entity_id), True, (255, 255, 255))  # Convertit l'ID en texte

        text_rect = text_surface.get_rect(center=(self.x, self.y))  # Centre du texte sur la créature
        window.blit(text_surface, text_rect)

    def display_vision(self, window):
        points = [(self.x, self.y)]
        num_points = 30
        start_angle = self.orientation - self.vision_angle / 2
        end_angle = self.orientation + self.vision_angle / 2
        for i in range(num_points + 1):
            angle = start_angle + (end_angle - start_angle) * i / num_points
            x = self.x + int(self.vision_range * math.cos(math.radians(angle)))
            y = self.y + int(self.vision_range * math.sin(math.radians(angle)))
            points.append((x, y))

        pygame.draw.polygon(window, (200, 200, 200), points)


