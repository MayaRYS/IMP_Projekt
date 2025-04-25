import pygame, sys
from settings import *
from menu_quit import Option

class main_menu:
    def __init__ (self,toggle_menu):
        pygame.display.set_caption("Menu")
        self.background = pygame.image.load ('../graphics/startbildschirm/startbild2.png')
        self.options = [Option('Quit', 390, 600, toggle_menu, quit_menu), Option('Play', 640, 600, toggle_menu, play_game), Option('Options', 890, 600, toggle_menu, None)]
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for option in self.options:
            option.check_hover(mouse_pos)
            option.check_click(mouse_pos, mouse_pressed)
            option.draw()

    
    def update(self):
        self.display_surface.blit(self.background, (0, 0))
        self.input()

def play_game(self):
    pygame.display.set_caption("Game")
    # self.start_active = False
    self.toggle_menu()

def quit_menu(self):
    pygame.quit()
    sys.exit()