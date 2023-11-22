import math
import pygame
import random
from pygame.surface import Surface
from typing import Tuple
from pdb import set_trace as bp
import time
from timeMeasure import TimeMeasure
from constants import *

class Entity:
    all_entities = []
    entity_id = 0
    time_measure = TimeMeasure()
    
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

        self.entity_id = Entity.entity_id
        Entity.entity_id += 1
        Entity.all_entities.append(self)

    def move(self):
        old_x = self.x
        old_y = self.y
        entities = Entity.get_all_entities()

        self.detect_entities(entities)

        ## Give random orientation and speed
        radian_angle = math.radians(self.orientation)  # Conversion en radians
        magnitude = random.uniform(0, 1)

        self.x = self.x + self.speed * magnitude * math.cos(radian_angle)
        self.y = self.y + self.speed * magnitude * math.sin(radian_angle)
        if self.time_since_last_orient_change >= ORIENT_CHANGE_DELAY:
            _, self.orientation = divmod(self.orientation + random.randint(-self.allowed_angle, self.allowed_angle), 360)
            self.time_since_last_orient_change = 0

        ## Take action
        collided_entity = self.collide_with(entities)
        if collided_entity:
            if self.is_predator() and collided_entity.is_prey():
                #self.size += 1
                collided_entity.killed()
                self.give_birth()
            elif self.is_prey() and collided_entity.is_food():
                #self.size += 1
                collided_entity.killed()
                self.give_birth()
                
        ## Check for collision 
        if self.is_window_collision() or collided_entity:
            self.x = old_x
            self.y = old_y
        
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
        self.remove_entity()

    def draw(self, window):
        self.display_vision(window)
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)
        self.draw_id(window)

    def draw_id(self, window):
        font = pygame.font.Font(None, 20)
        text_surface = font.render(str(self.entity_id), True, (255, 255, 255))  # Convertit l'ID en texte

        text_rect = text_surface.get_rect(center=(self.x, self.y))  # Centre du texte sur la créature
        window.blit(text_surface, text_rect)

    def is_window_collision(self):
        if self.x < 0 + self.size or self.x + self.size > WINDOW_WIDTH or self.y < 0 + self.size or self.y + self.size > WINDOW_HEIGHT:
            return True
        return False
     
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
                    return other_entity
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

    def remove_entity(self):
        try:
            Entity.all_entities.remove(self)
        except ValueError:
            pass
    
    def __del__(self):
        # Code executé avant d'etre supprimé ici
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
        entitites = Entity.get_all_entities()
        while self.collide_with(entitites) or self.is_window_collision():
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

    def display_infos(self):
        print(f"""\t{self.entity_type} id: {self.entity_id}\
              \n\t({self.x}, {self.y})\
              \n\tsize: {self.size}\
              \n\tspeed: {self.speed}\
              \n\tcolor: {self.color}\
              \n\tallowed_angle: {self.allowed_angle}\
              \n\torientation: {self.orientation}\
              \n\tdetected_entities: {[id.entity_id for id in self.detected_entities]}\
              \n\tEntity count: {len(Entity.get_all_entities())}\
              """)
        
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


