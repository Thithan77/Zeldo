import copy
import pygame
from math import *
from pygame.locals import *
class craftingTableInv:
    def __init__(self,InventoryTile):
        self.tab = []
        for i in range(5):
            self.tab.append([])
            for j in range(5):
                self.tab[i].append(copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["storage"]]))
        self.tab[0][0] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[1][0] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[2][0] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[3][0] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[4][0] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[3][1] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[4][1] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[3][2] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[3][3] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[4][3] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[0][4] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[1][4] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[2][4] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[3][4] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
        self.tab[4][4] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]])
    def add(self,what,hMany):
        print("no")