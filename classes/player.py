import pygame
class Player:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.texture = pygame.image.load("assets\\personnage jouable.png").convert_alpha()
        self.texture.set_colorkey((255,255,255))
