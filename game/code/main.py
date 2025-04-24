import pygame, sys
from settings import *
from level import Level
from menu_quit import *
from startbildschirm import main_menu
from timer import *

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Sprout land')
		self.clock = pygame.time.Clock()
		self.level = Level(self.toggle_start)
		self.main_menu = main_menu(self.toggle_start)
		self.start_active = True
 	
	def toggle_start(self):
		self.start_active = not self.start_active
		 
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
  
			if self.start_active == True:
 				
				self.main_menu.update()

			else:	
				dt = self.clock.tick() / 1000
				self.level.run(dt)
				
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()