import pygame, sys
from settings import *
from level import Level
from menu_quit import Menu_Quit

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Sprout land')
		self.clock = pygame.time.Clock()
		self.level = Level()

	def toggle_menu(self):
		self.menu_open = not self.menu_open

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
  
			dt = self.clock.tick() / 1000
			self.level.run(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()