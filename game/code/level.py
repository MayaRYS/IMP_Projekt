import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame # type: ignore
from support import *
from transition import *
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu
from menu_quit import Menu_Quit


class Level:
	def __init__(self, toggle_start):
		
		#clock
		self.clock = Clock(80, 55)
		
		self.first_setup = True

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()

		self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)

		#tent
		self.tent_active = False
		self.position_changed = False
		self.setup_tent = False
		self.setup_outside = False
		self.transition_plays = False
		
		self.setup()

		self.transition_tent = TransitionTent(self.position_changed, self.toggle_setup_tent, self.transition_plays)
		self.transition = Transition(self.reset, self.player)

		self.overlay = Overlay(self.player)

		# sky
		self.rain = Rain(self.all_sprites)
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		self.sky = Sky()

		# shop
		self.menu = Menu(self.player, self.toggle_shop)
		self.shop_active = False

		# quit

		self.menu_quit = Menu_Quit(self.toggle_menu_quit, toggle_start)
		self.menu_quit_active = False

		self.esc_pressed = False

	def setup(self):
		tmx_data = load_pygame('../data/map.tmx')

		self.all_sprites.empty()
		self.collision_sprites.empty()
		self.interaction_sprites.empty()

		"""
		# house 
		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

		for layer in ['HouseWalls', 'HouseFurnitureTop']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites)

		# Fence
		for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])
		"""
		# water 
		water_frames = import_folder('../graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)
		
		"""
		# trees 
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(
				pos = (obj.x, obj.y), 
				surf = obj.image, 
				groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], 
				name = obj.name,
				player_add = self.player_add)
		"""
		
		# wildflowers 
		for obj in tmx_data.get_layer_by_name('Objects'):
			WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

		for obj in tmx_data.get_layer_by_name('CollisionObj'):
			Generic((obj.x, obj.y), pygame.Surface((obj.width,obj.height)), self.collision_sprites)

		# Player 
			
		if self.first_setup:
			for obj in tmx_data.get_layer_by_name('Player'):
				if obj.name == "Start":
					self.player = Player(
							(obj.x,obj.y), 
							self.all_sprites, 
							self.collision_sprites,
							self.tree_sprites,
							self.interaction_sprites,
							self.soil_layer,
							self.toggle_shop,
							self.toggle_tent,
							self.toggle_position,
							self.tent_active, self.position_changed, self.toggle_transition)
				self.first_setup = False
				self.setup_outside = False
				
				if obj.name == 'Tent':
					Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

				if obj.name == 'Trader':
					Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)
		else:
			for obj in tmx_data.get_layer_by_name('Player'):
				if obj.name == "Start_exit_tent":
					self.player = Player(
							(obj.x,obj.y), 
							self.all_sprites, 
							self.collision_sprites,
							self.tree_sprites,
							self.interaction_sprites,
							self.soil_layer,
							self.toggle_shop,
							self.toggle_tent,
							self.toggle_position,
							self.tent_active, self.position_changed, self.toggle_transition)
					
				self.setup_outside = False
				
				if obj.name == 'Tent':
					Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

				if obj.name == 'Trader':
					Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

		Generic(
			pos = (0,0),
			surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])
		
		Generic(
			pos = (0,0),
			surf = pygame.image.load('../graphics/world/water.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['water'])
		
	def tent_setup(self):

		self.all_sprites.empty()
		self.collision_sprites.empty()
		self.interaction_sprites.empty()

		tmx_data = load_pygame('../data/tent.tmx')
		

		# wildflowers 
		for obj in tmx_data.get_layer_by_name('Objects'):
			WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])
		
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic(
				((x * TILE_SIZE +10), (y * TILE_SIZE -70)),
				surf,
				self.collision_sprites              
			)

		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					(obj.x, obj.y),
					self.all_sprites,
					self.collision_sprites,
					self.tree_sprites,
					self.interaction_sprites,
					self.soil_layer,
					self.toggle_shop,
					self.toggle_tent,
					self.toggle_position,
					self.tent_active, self.position_changed, self.toggle_transition)
				
				self.setup_tent = False
			
			if obj.name == 'Bed':
					Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Exit':
					Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)
			
		Generic(
			pos = (0,0),
			surf = pygame.image.load('../graphics/world/tent.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])
		
	def toggle_transition(self):
		self.transition_plays = not self.transition_plays
		self.set_transitions()

	def set_transitions(self):
		self.transition_tent = TransitionTent(self.position_changed, self.toggle_setup_tent, self.toggle_transition)
		self.transition = Transition(self.reset, self.player)
		self.transition_outside = TransitionOutside(self.toggle_setup_outside, self.toggle_transition)

	def toggle_setup_tent(self):
		self.setup_tent = not self.setup_tent

	def toggle_setup_outside(self):
		self.setup_outside = not self.setup_outside

	def toggle_position(self):
		self.position_changed = not self.position_changed

	def toggle_tent(self):
		self.tent_active = not self.tent_active

	def player_add(self,item):

		self.player.item_inventory[item] += 1

	def toggle_shop(self):

		self.shop_active = not self.shop_active

	def toggle_menu_quit(self):
		
		self.menu_quit_active = not self.menu_quit_active

	def reset(self):
		# plants
		self.soil_layer.update_plants()

		# soil
		self.soil_layer.remove_water()
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		if self.raining:
			self.soil_layer.water_all()

		# apples on the trees
		for tree in self.tree_sprites.sprites():
			for apple in tree.apple_sprites.sprites():
				apple.kill()
			tree.create_fruit()

		# sky
		self.sky.start_color = [255,255,255]

		#time
		self.clock = Clock(80, 55)

	def plant_collision(self):
		if self.soil_layer.plant_sprites:
			for plant in self.soil_layer.plant_sprites.sprites():
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
					self.player_add(plant.plant_type)
					plant.kill()
					Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
					self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

	def run(self,dt):

		keys = pygame.key.get_pressed()

		if self.setup_tent:
			self.tent_setup()
		elif self.setup_outside:
			self.setup()

		# hintergrund
		if self.tent_active:
			self.display_surface.fill('#000000')
		elif not self.transition_plays:
			self.display_surface.fill('#b8d43c')

		self.all_sprites.custom_draw(self.player)
		
		if keys[pygame.K_ESCAPE] and not self.esc_pressed:
			self.toggle_menu_quit()
			self.esc_pressed = True
		if not keys[pygame.K_ESCAPE]:
			self.esc_pressed = False

		
		if self.menu_quit_active:
			self.menu_quit.update()

		elif self.shop_active:
			self.menu.update()
			self.esc_pressed = True

		else:
			self.all_sprites.update(dt)
			self.clock.update(dt)
			self.plant_collision()

		
		self.overlay.display()

		if self.raining and not self.shop_active and not self.menu_quit_active and not self.tent_active:
			self.rain.update()

		self.sky.display(dt)
		
		if self.position_changed:
			if self.tent_active: 
				self.set_transitions()
				self.position_changed = False
			else:
				self.set_transitions()
				#self.setup()
				self.position_changed = False

		if self.transition_plays:
			if self.tent_active:
				self.transition_tent.play()
			else:
				self.transition_outside.play()
		elif self.player.sleep:
			self.transition.play()			

class Clock:
	def __init__(self, x, y):
		self.hour = 14
		self.minute = "00"
		self.clock = 0
		self.hour_full = True

		self.text = f"{str(self.hour)}:{self.minute}"
		self.color = 'Black'
		self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

		self.background = pygame.image.load('../graphics/menu/menu.png')
		self.background = pygame.transform.scale(self.background, (120, 66))  

		self.text_surf = self.font.render(self.text, False, self.color)
		self.rect = self.text_surf.get_rect(center=(x, y))
		self.display_surface = pygame.display.get_surface()

		self.x = x
		self.y = y

	def update(self, dt):
		self.clock += 2 * dt

		if (int(self.clock)/30) == 24:
			self.clock = 0
			self.hour = 0
			self.minute = "00"
			self.hour_full = True

		if ((int(self.clock)/30)%2) == 1 and self.hour_full:
			self.minute = "30"
			self.hour_full = False
		elif ((int(self.clock)/30)%2) == 0 and not self.hour_full:
			self.hour +=1
			self.minute = "00"
			self.hour_full = True

		self.draw()

	def draw(self):
		self.display_surface.blit(self.background, (self.x-60, self.y-32))
		self.text = f"{str(self.hour)}:{self.minute}"
		self.text_surf = self.font.render(self.text, False, self.color)
		self.display_surface.blit(self.text_surf, self.rect)

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)

					# # anaytics
					# if sprite == player:
					# 	pygame.draw.rect(self.display_surface,'red',offset_rect,5)
					# 	hitbox_rect = player.hitbox.copy()
					# 	hitbox_rect.center = offset_rect.center
					# 	pygame.draw.rect(self.display_surface,'green',hitbox_rect,5)
					# 	target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
					# 	pygame.draw.circle(self.display_surface,'blue',target_pos,5)