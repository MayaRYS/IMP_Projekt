import pygame
from settings import *
import time
from timer import Timer

class Menu_Quit:
    def __init__(self, toggle_menu):
        self.toggle_menu = toggle_menu
        self.options = [Option('Quit', 60, 55, quit)]
        self.timer = Timer(200)

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        for option in self.options:
            option.check_hover(mouse_pos)
            option.check_click(mouse_pos, mouse_pressed)
            option.draw()

    def update(self):
        self.input()

class Option:
    def __init__(self, text, x, y, action=None):
        self.text = text
        self.action = action
        self.color = 'Black'
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        self.background = pygame.image.load('../graphics/menu/menu.png')
        self.background = pygame.transform.scale(self.background, (97, 66))  

        self.text_surf = self.font.render(self.text, False, self.color)
        self.rect = self.text_surf.get_rect(center=(x, y))
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        self.display_surface.blit(self.background, (10, 20))

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
                self.action()

