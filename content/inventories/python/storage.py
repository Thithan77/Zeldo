import sys
import pygame
import copy
sys.path.insert(1,"../../../")
from classes.InventoryTile import *
class storage(InventoryTile):
    def __init__(self,Item):
        self.Item = Item
        super().__init__("storage",fileName="Inventaire_Objet.png")
        self.item = None
        self.count = 0
        self.font = pygame.font.SysFont(None, 14)
    def click(self,inventory):
        print("Click storage")
    def get_texture(self):
        texture = copy.copy(self.texture)
        if(self.item != None):
            o = self.Item.items[self.Item.nameToNumber[self.item]].texture # la texture de l'item contenu
            s = pygame.transform.scale(o,(24,24)) # On resize en plus petit pour tenir dans la case
            texture.blit(s,(4,4))
            img = self.font.render(str(self.count), True, (255,255,255))
            texture.blit(img, (24, 20))
        return texture
