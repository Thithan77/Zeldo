from classes.Tile import *
import yaml
import os
import sys
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
if(sys.platform == "linux"):
    files = os.listdir("content/tiles")
else:
    files = os.listdir("content\\tiles")
for i in files:
    print(i)
    if(sys.platform == "linux"):
        inf = yaml.load(open("content/tiles/"+i,"r"),Loader=Loader)
    else:
        inf = yaml.load(open("content\\tiles\\"+i,"r"),Loader=Loader)
    if(inf["doPass"] == True):
        inf["doPass"] = True
    else:
        inf["doPass"] = False
    Tile(inf["name"],inf)
for i in Tile.tiles:
    print(i.toString())

from classes.Item import *
if(sys.platform == "linux"):
    files = os.listdir("content/items")
else:
    files = os.listdir("content\\items")
for i in files:
    print(i)
    if(sys.platform == "linux"):
        inf = yaml.load(open("content/items/"+i,"r"),Loader=Loader)
    else:
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
from content.inventories.python.storage_babouche import *
storage(Item)
from content.inventories.python.storage_chest import *
storage(Item)
from content.inventories.python.storage_jambiere import *
storage(Item)
from content.inventories.python.storage_helmet import *
storage(Item)
from classes.inventories import *
Inventory(InventoryTile)
def it():
    """
    Retourne InventoryTile
    """
    return InventoryTile


