import copy
import pygame
from math import *
from pygame.locals import *
class Inventory:
    def __init__(self,InventoryTile):
        print(InventoryTile.tiles[0].name)
        self.tab = []
        for i in range(9):
            self.tab.append([])
            for j in range(9):
                self.tab[i].append(copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["void"]]))
        self.tab[4][4] = copy.copy(InventoryTile.tiles[InventoryTile.nameToNumber["button"]])
def open_inventory(fen,inventory,options,player,Tile,map):
    inv_open = True
    while inv_open:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                inv_open = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    inv_open = False
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                cx = x-(options["fen"]["width"] - 9*32)
                cy = y-(options["fen"]["height"] - 9*32)
                print((int(cx/32),int(cy/32)))
                inventory.tab[int(cx/32)][int(cy/32)].click(inventory)
        col = int(options["fen"]["height"]//32+3)
        lin = int(options["fen"]["width"]//32+3)
        xmin = player.x*32-(options["fen"]["width"]/2)+32
        ymin = player.y*32-(options["fen"]["height"]/2)+32
        x = xmin
        y = ymin
        for i in range(col):
            yc = y%32
            for j in range(lin):
                xc = x%32
                if(floor(x/32) <= 0 or floor(y/32) <= 0 or floor(x/32) >= 200 or floor(y/32) >= 200):
                    fen.blit(Tile.tiles[Tile.nameToNumber["darkeau"]].texture,(j*32-xc,i*32-yc))
                else:
                    yz = floor(y/32)
                    xz = floor(x/32)
                    if(map.gm(int(xz-1),int(yz-1))%1 == 0):
                        texture = Tile.tiles[map.gm(int(xz-1),int(yz-1))].texture
                        fen.blit(texture,((j)*32-xc,(i)*32-yc))
                    else:
                        rot = int(map.gm(int(xz-1),int(yz-1))%1*10)
                        #print(rot)
                        texture = Tile.tiles[int(map.gm(int(xz-1),int(yz-1))//1)].textures[rot]
                        fen.blit(texture,((j)*32-xc,(i)*32-yc))
                    if(Tile.tiles[map.gs(int(xz-1),int(yz-1))].name != "nada"):
                        texture = Tile.tiles[map.gs(int(xz-1),int(yz-1))].texture
                        fen.blit(texture,((j)*32-xc,(i)*32-yc))
                x+=32
            x = xmin
            y+=32
        for i in range(9):
            for j in range(9):
                xl = i*32
                yl = j*32
                x = options["fen"]["width"] - 9*32 + xl
                y = options["fen"]["height"] - 9*32 + yl
                fen.blit(inventory.tab[i][j].get_texture(),(x,y))
        fen.blit(player.texture,(options["fen"]["width"]/2-16,options["fen"]["height"]/2-16))
        map.draw_others(fen,player,options)
        pygame.display.flip()
