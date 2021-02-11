#coding:utf-8
# Définition de la classe Tile
import pygame
class Tile:
    n = 0 #Indique le nombre d'instances aka le nombre de tiles qu'on a (permet de définir des ids dynamiques sans problème)
    nameToNumber = {} # Un dictionnaire qui associe le nom à l'id
    tiles = [] # la liste de toutes les instances
    def __init__(self,name,opt={},**opt2): # Opt = Un dictionnaire {clé:valeur} qui contient la liste des options
        opt.update(opt2) # On fusionne les deux dictionnaires
        Tile.tiles.append(self)
        self.name = name # Le nom de la tile
        self.id = Tile.n;Tile.n+=1 #On définit l'id au compteur actuel et on incrémente de 1
        Tile.nameToNumber[self.name] = self.id
        if("doPass" in opt): # Le bloc est-il traversable ?
            self.doPass = opt["doPass"]
        else:
            self.doPass = True
        if("speed" in opt): # la vitesse du personnage entre 0 et 1
            self.speed = opt["speed"]
        else:
            self.speed = 0.1
        if("type" in opt): # Le bloc est-il dans le fond ou au devant
            self.type = opt["type"]
        else:
            self.type = "map"
        if("fileName" in opt):
            self.fileName = opt["fileName"]
            self.texture2 = pygame.image.load("assets\\"+opt["fileName"]).convert_alpha()
            self.texture2.set_colorkey((255,255,255))
            self.texture = pygame.Surface((32,32)).convert_alpha()
            self.texture.fill((0,0,0,0))
            self.texture.blit(self.texture2,(0,0,32,32))
        else:
            self.fileName = None
            self.texture = pygame.Surface((32,32)).fill((255,255,255))
    def toString(self): # Renvoie toutes les informations sous forme de texte (pour le débug principalement)
        return("{} , id:{}".format(self.name,self.id))

# Exemple d'instanciation
if __name__ == "__main__":
    opt = {"name":"Pierre","doPass":False}
    Tile(opt)
    opt = {"name":"Herbe","doPass":True}
    Tile(opt)
