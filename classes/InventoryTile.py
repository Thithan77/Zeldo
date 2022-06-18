import pygame
import sys
class InventoryTile:
    n = 0 #Indique le nombre d'instances aka le nombre de tiles qu'on a (permet de définir des ids dynamiques sans problème)
    nameToNumber = {} # Un dictionnaire qui associe le nom à l'id
    tiles = [] # la liste de toutes les instances
    def __init__(self,name,opt={},**opt2):
        opt.update(opt2)
        InventoryTile.tiles.append(self)
        self.name = name
        self.id = InventoryTile.n;InventoryTile.n+=1
        InventoryTile.nameToNumber[self.name] = self.id
        if("fileName" in opt):
            self.fileName = opt["fileName"]
            if(sys.platform == "linux"):
                self.texture2 = pygame.image.load("assets/"+opt["fileName"]).convert()
            else:
                self.texture2 = pygame.image.load("assets\\"+opt["fileName"]).convert()
            self.texture2.set_colorkey((255,255,255))
            self.texture = pygame.Surface((32,32)).convert_alpha()
            self.texture.fill((0,0,0,0))
            self.texture.blit(self.texture2,(0,0,32,32))
            if("rotation" in opt and opt["rotation"]):
                self.textures = []
                for i in [(False,False),(False,True),(True,True),(True,False)]:
                    texture = pygame.transform.flip(self.texture,i[0],i[1])
                    self.textures.append(texture)
        else:
            self.fileName = None
            self.texture = pygame.Surface((32,32)).fill((255,255,255))
    def click(self,inventory):
        print("Clicked !")
    def get_texture(self):
        return self.texture
    def delTexture(self):
        del self.texture
        del self.texture2
    def reloadTexture(self):
        if(self.fileName):
            if(sys.platform == "linux"):
                self.texture2 = pygame.image.load("assets/"+self.fileName).convert()
            else:
                self.texture2 = pygame.image.load("assets\\"+self.fileName).convert()
            self.texture2.set_colorkey((255,255,255))
            self.texture = pygame.Surface((32,32)).convert_alpha()
            self.texture.fill((0,0,0,0))
            self.texture.blit(self.texture2,(0,0,32,32))
            """
            if("rotation" in opt and opt["rotation"]):
                self.textures = []
                for i in [(False,False),(False,True),(True,True),(True,False)]:
                    texture = pygame.transform.flip(self.texture,i[0],i[1])
                    self.textures.append(texture)
            """
        else:
            self.fileName = None
            self.texture = pygame.Surface((32,32)).fill((255,255,255))