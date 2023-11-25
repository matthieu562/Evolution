import time
since_started_clock = time.time()
from entity import Entity
from grid import Grid
from prey import Prey
from predator import Predator
from food import Food

# from predator import Predator
# from prey import Prey
import pygame
import random
from pdb import set_trace as bp
from constants import *

pygame.init()

# Taille de la fenêtre
# WINDOW_WIDTH = 800 #1700
# WINDOW_HEIGHT = 600 #850

# Création de la fenêtre
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulation prédateurs et proies")
clock = pygame.time.Clock()

def find_index_by_id(target_id):
    for index, entity in enumerate(Entity.get_all_entities()):
        if entity.entity_id == target_id:
            return index  
    return -1  

_ = [Food(
        # window,
        x=random.randint(0, WINDOW_WIDTH),
        y=random.randint(0, WINDOW_HEIGHT),
        size=random.randint(ENTITY_MIN_SIZE, ENTITY_MAX_SIZE),
        speed=0,
        color=(0, random.randint(ENTITY_MIN_COLOR, ENTITY_MAX_COLOR), 0),
        allowed_angle=0,
        orientation=0,
        time_since_last_birth=0,
        reproduction_delay=random.randint(MIN_REPRODUCTION_DELAY, MAX_REPRODUCTION_DELAY)
        ) for _ in range(NB_FOOD)
    ]

_ = [Prey(
        # window,
        x=random.randint(0, WINDOW_WIDTH),
        y=random.randint(0, WINDOW_HEIGHT),
        size=random.randint(ENTITY_MIN_SIZE, ENTITY_MAX_SIZE),
        speed=random.randint(ENTITY_MIN_SPEED, ENTITY_MAX_SPEED),
        color=(0, 0, random.randint(ENTITY_MIN_COLOR, ENTITY_MAX_COLOR)),
        allowed_angle=random.randint(PREY_MIN_ALLOWED_ANGLE, PREY_MAX_ALLOWED_ANGLE),
        orientation=random.randint(0, 359),
        reproduction_delay=random.randint(MIN_REPRODUCTION_DELAY, MAX_REPRODUCTION_DELAY),
        vision_angle=random.randint(PREY_MIN_VISION_ANGLE, PREY_MAX_VISION_ANGLE),
        vision_range=random.randint(PREY_MIN_VISION_RANGE, PREY_MAX_VISION_RANGE)
        ) for _ in range(NB_PREYS)
    ]

_ = [Predator(
        # window,
        x=random.randint(0, WINDOW_WIDTH),
        y=random.randint(0, WINDOW_HEIGHT),
        size=random.randint(ENTITY_MIN_SIZE, ENTITY_MAX_SIZE),
        speed=random.randint(ENTITY_MIN_SPEED, ENTITY_MAX_SPEED),
        color=(random.randint(ENTITY_MIN_COLOR, ENTITY_MAX_COLOR), 0, 0),
        allowed_angle=random.randint(PREDATOR_MIN_ALLOWED_ANGLE, PREDATOR_MAX_ALLOWED_ANGLE),
        orientation=random.randint(0, 359),
        reproduction_delay=random.randint(MIN_REPRODUCTION_DELAY, MAX_REPRODUCTION_DELAY),
        vision_angle=random.randint(PREDATOR_MIN_VISION_ANGLE, PREDATOR_MAX_VISION_ANGLE),
        vision_range=random.randint(PREDATOR_MIN_VISION_RANGE, PREDATOR_MAX_VISION_RANGE)
        ) for _ in range(NB_PREDATORS)
    ]

new_food_spawn_clock = 0
grid_content_old = {}
scoreboard_delay = 0
running = True
frame_by_frame = True
is_first_loop_top = True
is_first_loop_bottom = True
while running:
    window.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                frame_by_frame = not frame_by_frame  # Inverser l'état frame par frame
            elif event.key == pygame.K_p:
                bp()

    if frame_by_frame:  # Vérifier si le mode frame par frame est activé
        entities = Entity.get_all_entities()
        preys = Entity.get_all_preys()
        predators = Entity.get_all_predators()
        foods = Entity.get_all_foods()

        # Grid management
        # grid = Grid(100, 200, 30, 30, {})
        # grid.display_grid(window)
        if is_first_loop_top:
            Grid.create_grid()
            # for grid in Grid.get_all_grids():
            #     grid.initialize_content(entities)
        is_first_loop_top = False
                
        for grid in Grid.get_all_grids():
            grid_content = Entity.grid_content
        # if grid_content != grid_content_old:
            #grid.draw(window, grid_content)
        # grid_content_old = grid_content

        if scoreboard_delay >= 2 * GAME_FREQ:
            print(' ')
            print('entities', len(entities))
            print('preys', len(preys))
            print('predators', len(predators))
            print('foods', len(foods))
            # print('move_time:', Entity.move_time)
            # print('collide_with_time:', Entity.collide_with_time)
            # print('get_all_entities_time:', Entity.get_all_entities_time)
            print('since_started_clock:', time.time() - since_started_clock)
            # print('GAME_CLOCK:', GAME_CLOCK)
            scoreboard_delay = 0

        for prey in preys:
            prey.move()
            prey.update_status()
            prey.draw(window)
        
        for predator in predators:
            predator.move()
            predator.update_status()
            predator.draw(window)
        
        for food in foods:
            #food.move()
            food.update_status()
            food.draw(window)
        
        #print(Entity.grid_content, '\n')
        
        ## Random coords food spawn
        if new_food_spawn_clock >= FOOD_SPAWN_DELAY:
            _ = [Food(
                    # window,
                    x=random.randint( 0, WINDOW_WIDTH),
                    y=random.randint(0, WINDOW_HEIGHT),
                    size=random.randint(ENTITY_MIN_SIZE, ENTITY_MAX_SIZE),
                    speed=0,
                    color=(0, random.randint(ENTITY_MIN_COLOR, ENTITY_MAX_COLOR), 0),
                    # allowed_angle=0,
                    # orientation=0,
                    time_since_last_birth=0,
                    reproduction_delay=random.randint(MIN_REPRODUCTION_DELAY, MAX_REPRODUCTION_DELAY)
                    ) for _ in range(FOOD_SPAWN_AMOUNT)
                ]
            new_food_spawn_clock = 0

        ## Update clocks and times
        for entity in entities:
            ## Bug, entities disappear and re-appear randomly
            # entity.update_status()
            # entity.move()
            # entity.draw(window)
            entity.update_time_properties()
        new_food_spawn_clock += 1
        scoreboard_delay += 1
        GAME_CLOCK += 1

        pygame.display.update() # update only changed pixel (si jai bien capté)
        #pygame.display.flip() # refresh tout

    clock.tick(GAME_FREQ)

    if is_first_loop_bottom:
        # Change this bool to freeze at start
        frame_by_frame = True
    is_first_loop_bottom = False

pygame.quit()



"""
Debug command:

find_index_by_id(69)
Entity.get_all_entities()[55].detect_entities(Entity.get_all_entities())
Entity.get_all_entities()[find_index_by_id(69)].display_infos()

y a des ptis bugs sur la vision encore, genre la salade n'est pas détécté mais pas que 

"""
