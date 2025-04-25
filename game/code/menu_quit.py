import pygame
from settings import *
import time
from timer import Timer

class Menu_Quit:
    def __init__(self, toggle_menu_quit, toggle_menu):
        self.toggle_menu_quit = toggle_menu_quit
        self.options = [Option('Quit', 60, 55, toggle_menu, self.quit_game)]
        self.timer = Timer(200)
        self.toggle_menu = toggle_menu

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        for option in self.options:
            option.check_hover(mouse_pos)
            option.check_click(mouse_pos, mouse_pressed)
            option.draw()

    def update(self):
        self.input()

    def quit_game(self, toggle_menu):
        self.toggle_menu_quit()
        self.toggle_menu()

class Option:
    def __init__(self, text, x, y, toggle_menu, action=None):
        self.text = text
        self.action = action
        self.color = 'Black'
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        self.background = pygame.image.load('../graphics/menu/menu.png')
        self.background = pygame.transform.scale(self.background, (120, 66))  

        self.text_surf = self.font.render(self.text, False, self.color)
        self.rect = self.text_surf.get_rect(center=(x, y))
        self.display_surface = pygame.display.get_surface()

        self.toggle_menu = toggle_menu
        self.x = x
        self.y = y

    def draw(self):
        self.display_surface.blit(self.background, (self.x-60, self.y-32))

        self.text_surf = self.font.render(self.text, False, self.color)
        self.display_surface.blit(self.text_surf, self.rect)

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.color = 'White'
        else:
            self.color = 'Black'

    def check_click(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            if self.action:
                self.action(self)

