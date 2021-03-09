from classes.Tile import *
import yaml
import os
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
files = os.listdir("content\\tiles")
for i in files:
    print(i)
    inf = yaml.load(open("content\\tiles\\"+i,"r"),Loader=Loader)
    if(inf["doPass"] == True):
        inf["doPass"] = True
    else:
        inf["doPass"] = False
    Tile(inf["name"],inf)
for i in Tile.tiles:
    print(i.toString())

from classes.Item import *
files = os.listdir("content\\items")
for i in files:
    print(i)
    inf = yaml.load(open("content\\items\\"+i,"r"),Loader=Loader)
    Item(inf["name"],inf)
for i in Item.items:
    print(i.toString())


# Le système d'inventaire
from classes.InventoryTile import *
from content.inventories.python.void import *
void()
from content.inventories.python.storage import *
storage(Item)
from content.inventories.python.button import *
button()
from classes.inventories import *
Inventory(InventoryTile)
def it():
    """
    Retourne InventoryTile
    """
    return InventoryTile
