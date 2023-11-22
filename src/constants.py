
# READ ONLY VARIABLES (except GAME_CLOCK that is incremented in game loop)

# window
WINDOW_WIDTH = 1700
WINDOW_HEIGHT = 850
BACKGROUND = (0, 0, 0)

# Frequence
GAME_CLOCK = 0
GAME_FREQ = 30

# General species properties
NB_PREDATORS = 20
NB_PREYS = 80
NB_FOOD = 50

PREDATORS_LIVETIME = 20 * GAME_FREQ
PREYS_LIVETIME = 30 * GAME_FREQ

## Species properties
# General
ENTITY_MIN_SIZE = 7
ENTITY_MAX_SIZE = 20

ENTITY_MIN_SPEED = 2
ENTITY_MAX_SPEED = 6

ENTITY_MIN_COLOR = 100
ENTITY_MAX_COLOR = 255

MIN_REPRODUCTION_DELAY = 10 * GAME_FREQ
MAX_REPRODUCTION_DELAY = 30 * GAME_FREQ
ORIENT_CHANGE_DELAY = 0.1 * GAME_FREQ

# Foods
FOOD_SPAWN_DELAY = 10 * GAME_FREQ
FOOD_SPAWN_AMOUNT = 2
FOOD_MAX_UNITS = 200

FOOD_MIN_COLOR = 100
FOOD_MAX_COLOR = 255

FOOD_MIN_SIZE = 7
FOOD_MAX_SIZE = 20

# Preys
PREY_MIN_ALLOWED_ANGLE = 20 
PREY_MAX_ALLOWED_ANGLE = 60

PREY_MIN_VISION_ANGLE = 20 
PREY_MAX_VISION_ANGLE = 80

PREY_MIN_VISION_RANGE = 70
PREY_MAX_VISION_RANGE = 100

# Predators
PREDATOR_MIN_ALLOWED_ANGLE = 20 
PREDATOR_MAX_ALLOWED_ANGLE = 45

PREDATOR_MIN_VISION_ANGLE = 20 
PREDATOR_MAX_VISION_ANGLE = 60

PREDATOR_MIN_VISION_RANGE = 60
PREDATOR_MAX_VISION_RANGE = 90