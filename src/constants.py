
# READ ONLY VARIABLES (except GAME_CLOCK that is incremented in game loop)

# window
WINDOW_WIDTH = 1680 # px
WINDOW_HEIGHT = 880 # px
# WINDOW_WIDTH = 160 # px
# WINDOW_HEIGHT = 160 # px
BACKGROUND = (0, 0, 0)  # over 255

# Frequence
GAME_CLOCK = 0 # qty : quantity
SPEED_FACTOR = 1
GAME_FREQ = 30 * SPEED_FACTOR # Hz

# General species properties
NB_PREDATORS = 10 # qty
NB_PREYS = 80 # qty
NB_FOOD = 30 # qty
# NB_PREDATORS = 0 # qty
# NB_PREYS = 2 # qty
# NB_FOOD = 2 # qty

PREDATORS_LIVETIME = 20 * GAME_FREQ # frame
PREYS_LIVETIME = 30 * GAME_FREQ # frame

## Species properties
# General
ENTITY_MIN_SIZE = 7 # pixel, radius
ENTITY_MAX_SIZE = 20 # pixel, radius

ENTITY_MIN_SPEED = 2 # px per frame
ENTITY_MAX_SPEED = 6 # px per frame

ENTITY_MIN_COLOR = 100 # over 255
ENTITY_MAX_COLOR = 255 # over 255

MIN_REPRODUCTION_DELAY = 10 * GAME_FREQ # frame
MAX_REPRODUCTION_DELAY = 30 * GAME_FREQ # frame
ORIENT_CHANGE_DELAY = 0.1 * GAME_FREQ # frame

# Foods
FOOD_SPAWN_DELAY = 5 * GAME_FREQ # frame
FOOD_SPAWN_AMOUNT = 2 # qty
FOOD_MAX_UNITS = 250 # qty

FOOD_MIN_COLOR = 100 # over 255
FOOD_MAX_COLOR = 255 # over 255

FOOD_MIN_SIZE = ENTITY_MIN_SIZE # pixel, radius
FOOD_MAX_SIZE = ENTITY_MAX_SIZE # pixel, radius

# Preys
PREY_MIN_ALLOWED_ANGLE = 20 # degrees
PREY_MAX_ALLOWED_ANGLE = 60 # degrees

PREY_MIN_VISION_ANGLE = 20 # degrees
PREY_MAX_VISION_ANGLE = 80 # degrees

PREY_MIN_VISION_RANGE = 70 # px
PREY_MAX_VISION_RANGE = 100 # px

# Predators
PREDATOR_MIN_ALLOWED_ANGLE = 20  # degrees
PREDATOR_MAX_ALLOWED_ANGLE = 45 # degrees

PREDATOR_MIN_VISION_ANGLE = 20 # degrees
PREDATOR_MAX_VISION_ANGLE = 60 # degrees

PREDATOR_MIN_VISION_RANGE = 60 # px
PREDATOR_MAX_VISION_RANGE = 90 # px

# Grid
GRID_COLOR = (150, 150, 150) # over 255