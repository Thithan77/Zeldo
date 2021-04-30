import pygame
import sys
class Craft:
    """

    """
    n = 0 #Indique le nombre d'instances aka le nombre de tiles qu'on a (permet de définir des ids dynamiques sans problème)
    nameToNumber = {} # Un dictionnaire qui associe le nom à l'id
    items = [] # la liste de toutes les instances
    def __init__(self,name,opt={},**opt2):
        opt.update(opt2)
        Craft.crafts.append(self)
        self.name = name
        self.id = Item.n;Item.n+=1
        Craft.nameToNumber[self.name] = self.id

    def toString(self): # Renvoie toutes les informations sous forme de texte (pour le débug principalement)
        return("{} , id:{}".format(self.name,self.id))
