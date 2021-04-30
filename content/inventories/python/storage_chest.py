import sys
import pygame
import copy
sys.path.insert(1,"../../../")
from classes.InventoryTile import *
class storage(InventoryTile):
    def __init__(self,Item):
        self.Item = Item
        super().__init__("storage_chest",fileName="inv_chest.png")
        self.item = None
        self.count = 0
        self.font = pygame.font.SysFont(None, 14)
        self.acceptItem = True
    def click(self,inventory):
        print("Click storage")
    def get_texture(self):
        texture = copy.copy(self.texture)
        if(self.item != None):
            o = self.Item.items[self.Item.nameToNumber[self.item]].texture # la texture de l'item contenu
            s = pygame.transform.scale(o,(32,32)) # On resize en plus petit pour tenir dans la case
            texture.blit(s,(0,0))
            img = self.font.render(str(self.count), True, (255,255,255))
            texture.blit(img, (24, 20))
        return texture
