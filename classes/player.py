import pygame
import sys
class Player:
    def __init__(self):
        self.x = 2
        self.y = 2
        if(sys.platform == "linux"):
            self.texture2 = pygame.image.load("assets/personnage jouable.png").convert()
        else:
            self.texture2 = pygame.image.load("assets\\personnage jouable.png").convert()
        self.texture2.set_colorkey((255,255,255))
        self.texture = pygame.Surface((32,32)).convert_alpha()
        self.texture.fill((0,0,0,0))
        self.texture.blit(self.texture2,(0,0,32,32))
