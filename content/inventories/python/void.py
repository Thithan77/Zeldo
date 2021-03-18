import sys
sys.path.insert(1,"../../../")
from classes.InventoryTile import *
class void(InventoryTile):
    def __init__(self):
        super().__init__("void",fileName="Inventaire_Vide.png")
    def click(self,inventory):
        print("Click void")
