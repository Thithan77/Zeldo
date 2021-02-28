import sys
import pygame
sys.path.insert(1,"../../../")
from classes.InventoryTile import *
class storage(InventoryTile):
    def __init__(self,Item):
        self.Item = Item
        super().__init__("storage",fileName="sable.png")
        self.item = "wood"
    def click(self,inventory):
        print("Click storage")
    def get_texture(self):
        texture = self.texture
        if(self.item != None):
            o = self.Item.items[self.Item.nameToNumber[self.item]].texture # la texture de l'item contenu
            s = pygame.transform.scale(o,(24,24)) # On resize en plus petit pour tenir dans la case
            texture.blit(s,(4,4))
        return texture
