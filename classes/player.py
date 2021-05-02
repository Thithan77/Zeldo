import pygame
import sys
class Player:
    def __init__(self):
        self.x = 2
        self.y = 2
        if(sys.platform == "linux"):
            self.texture2 = pygame.image.load("assets/personnage jouable.png").convert()
            self.back2 = pygame.image.load("assets/Personnage jouable dos.png").convert()
            self.droite2 = pygame.image.load("assets/zeldo_droite.png").convert()
            self.gauche2 = pygame.image.load("assets/zeldo_gauche.png").convert()
        else:
            self.texture2 = pygame.image.load("assets\\personnage jouable.png").convert()
            self.back2 = pygame.image.load("assets\\Personnage jouable dos.png").convert()
            self.droite2 = pygame.image.load("assets\\zeldo_droite.png").convert()
            self.gauche2 = pygame.image.load("assets\\zeldo_gauche.png").convert()
        self.texture2.set_colorkey((255,255,255))
        self.texture = pygame.Surface((32,32)).convert_alpha()
        self.texture.fill((0,0,0,0))
        self.texture.blit(self.texture2,(0,0,32,32))
        self.back2.set_colorkey((255,255,255))
        self.back = pygame.Surface((32,32)).convert_alpha()
        self.back.fill((0,0,0,0))
        self.back.blit(self.back2,(0,0,32,32))
        self.droite2.set_colorkey((255,255,255))
        self.droite = pygame.Surface((32,32)).convert_alpha()
        self.droite.fill((0,0,0,0))
        self.droite.blit(self.droite2,(0,0,32,32))
        self.gauche2.set_colorkey((255,255,255))
        self.gauche = pygame.Surface((32,32)).convert_alpha()
        self.gauche.fill((0,0,0,0))
        self.gauche.blit(self.gauche2,(0,0,32,32))
