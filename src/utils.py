from constants import *

def get_new_xy_on_grid(x, y):
    _, x_rest = divmod(x, 2 * ENTITY_MAX_SIZE)
    _, y_rest = divmod(y, 2 * ENTITY_MAX_SIZE)
    new_x_on_grid = x - x_rest
    new_y_on_grid = y - y_rest
    return int(new_x_on_grid), int(new_y_on_grid)

def get_key(x, y):
    return str(f'{x}x{y}y')

def get_keys(x, y):
    keys = []
    for x_index in range(-1, 2):
        for y_index in range(-1, 2):
            x_key = x + x_index * 2 * ENTITY_MAX_SIZE
            y_key = y + y_index * 2 * ENTITY_MAX_SIZE
            keys.append(get_key(x_key, y_key))
    return keys
        

