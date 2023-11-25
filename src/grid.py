from constants import *
import pygame
from pdb import set_trace as bp
from utils import get_new_xy_on_grid, get_key


class Grid:
    all_grids_list = []
    all_grids_dict = {}
    grid_id = 0
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # self.content = content # dict : {'XXXXxYYYYy':[entities]}
        
        self.grid_id = Grid.grid_id
        self.grid_id += 1
        
        x_on_grid, y_on_grid = get_new_xy_on_grid(x, y)
        key = get_key(x_on_grid, y_on_grid)
        Grid.all_grids_dict[key] = self
        Grid.all_grids_list.append(self)
        
    # # Run once at the beginning to fill all the grid with its content
    # def initialize_content(self, entities):
    #     # for entity in entities:
    #     #     if str(f'{entity.x}x{entity.y}y') not in self.content:
    #     #         self.content[str(f'{entity.x}x{entity.y}y')] = entity
    #     #     else:
    #     #         self.content[str(f'{entity.x}x{entity.y}y')] = entity
    #     for entity in entities:
    #         key = str(f'{entity.x_on_grid}x{entity.y_on_grid}y')
    #         # Si la clé existe déjà
    #         if key in self.content:
    #             # Si la valeur n'est pas une liste, la convertir en liste
    #             if not isinstance(self.content[key], list):
    #                 self.content[key] = [self.content[key]]
    #             # Ajouter la nouvelle valeur à la liste existante
    #             self.content[key].append(entity)
    #         else:
    #             # Si la clé n'existe pas, ajouter la nouvelle clé et sa valeur
    #             self.content[key] = entity

    # def get_grid_content(self):
    #     key = str(f'{self.x}x{self.y}y')
    #     if key in self.content:
    #         return self.content[key]
    #     else:
    #         return None

    @classmethod
    def create_grid(cls):
        nb_horizontal_grid = WINDOW_WIDTH / (2 * ENTITY_MAX_SIZE)
        nb_vertical_grid = WINDOW_HEIGHT / (2 * ENTITY_MAX_SIZE)
        
        if nb_horizontal_grid % 1 != 0 or nb_vertical_grid % 1 != 0:
            raise ValueError('WINDOW_WIDTH or WINDOW_HEIGHT not divisible by ENTITY_MAX_SIZE')

        for x in range(int(nb_horizontal_grid)):
            for y in range(int(nb_vertical_grid)):
                cls(x * (2 * ENTITY_MAX_SIZE), y * (2 * ENTITY_MAX_SIZE), (2 * ENTITY_MAX_SIZE), (2 * ENTITY_MAX_SIZE))

    @classmethod
    def get_all_grids(cls):
        return cls.all_grids_list
    
    def __str__(self):
        return (f"""\t({self.x},{self.y})\
              \n\tsize :({self.width}, {self.height})\
              \n\tEntity count: {len(Grid.get_all_grids())}\
              """)
        
    def draw(self, window, grid_content):
        if grid_content:
            Grid.fill_grid(window, grid_content)
        self.display_grid(window)
        self.display_id(window)


    def display_grid(self, window):
        pygame.draw.rect(window, GRID_COLOR, (self.x, self.y, self.width, self.height), True)
    
    def fill_grid(window, grid_content):
        # for grid in Grid.get_all_grids():
        #     x_on_grid, y_on_grid = get_new_xy_on_grid(grid.x, grid.y)
        #     key = get_key(x_on_grid, y_on_grid)
        for key, _ in grid_content.items():
            grid = Grid.all_grids_dict[key]
            if grid_content.get(key) is not None:
                if len(grid_content[key]) == 1:
                    pygame.draw.rect(window, (150, 100, 0), (grid.x, grid.y, grid.width, grid.height), False)
                elif len(grid_content[key]) > 1:
                    pygame.draw.rect(window, (255, 100, 0), (grid.x, grid.y, grid.width, grid.height), False)

    def display_id(self, window):
        font = pygame.font.Font(None, 15)
        
        text_surface1 = font.render(f'{self.x}', True, GRID_COLOR)  # Convertit l'ID en texte
        text_rect1 = text_surface1.get_rect(center=(self.x + self.width / 2, self.y + self.height / 4))  # Centre du texte sur la créature
        
        text_surface2 = font.render(f'{self.y}', True, GRID_COLOR)  # Convertit l'ID en texte
        text_rect2 = text_surface2.get_rect(center=(self.x + self.width / 2, self.y + self.height / 4 * 3))  # Centre du texte sur la créature

        window.blit(text_surface1, text_rect1)
        window.blit(text_surface2, text_rect2)


"""

len(Grid.get_all_grids())
"""