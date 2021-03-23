import sys
import pygame
sys.path.insert(1,"../../../")
from classes.InventoryTile import *
class button(InventoryTile):
    def __init__(self):
        super().__init__("button")
        if(sys.platform == "linux"):
            self.on = pygame.image.load("assets/bouton_on.png").convert_alpha()
            self.off = pygame.image.load("assets/bouton_off.png").convert_alpha()
        else:
            self.on = pygame.image.load("assets\\bouton_on.png").convert_alpha()
            self.off = pygame.image.load("assets\\bouton_off.png").convert_alpha()
        self.statut = "off"
    def click(self,inventory):
        if(self.statut == "off"):
            self.statut = "on"
        else:
            self.statut = "off"
    def get_texture(self):
        if(self.statut == "on"):
            texture = self.on
        else:
            texture = self.off
        return texture
