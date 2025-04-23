from pygame.math import Vector2
# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 120

# overlay positions 
OVERLAY_POSITIONS = {
	'tool' : (40, SCREEN_HEIGHT - 15), 
	'seed': (70, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

LAYERS = {
	'water': 0,
    'water_animation': 1,
	'ground': 2,
	'soil': 3,
	'soil water': 4,
	'rain floor': 5,
	'house bottom': 6,
	'ground plant': 7,
	'main': 8,
	'house top': 9,
	'fruit': 10,
	'rain drops': 11
}

APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}