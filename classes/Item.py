import pygame
class Item:
    n = 0 #Indique le nombre d'instances aka le nombre de tiles qu'on a (permet de définir des ids dynamiques sans problème)
    nameToNumber = {} # Un dictionnaire qui associe le nom à l'id
    items = [] # la liste de toutes les instances
    def __init__(self,name,opt={},**opt2):
        opt.update(opt2)
        Item.items.append(self)
        self.name = name
        self.id = Item.n;Item.n+=1
        Item.nameToNumber[self.name] = self.id
        if("fileName" in opt):
            self.fileName = opt["fileName"]
            self.texture2 = pygame.image.load("assets\\"+opt["fileName"]).convert()
            self.texture2.set_colorkey((255,255,255))
            self.texture = pygame.Surface((32,32)).convert_alpha()
            self.texture.fill((0,0,0,0))
            self.texture.blit(self.texture2,(0,0,32,32))
        else:
            self.fileName = None
            self.texture = pygame.Surface((32,32)).fill((255,255,255))
    def toString(self): # Renvoie toutes les informations sous forme de texte (pour le débug principalement)
        return("{} , id:{}".format(self.name,self.id))
