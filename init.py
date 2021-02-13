from classes.Tile import *
import yaml
import os
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
files = os.listdir("content\\tiles")
for i in files:
    inf = yaml.load(open("content\\tiles\\"+i,"r"),Loader=Loader)
    print(inf)
    if(inf["doPass"] == True):
        inf["doPass"] = True
    else:
        inf["doPass"] = False
    Tile(inf["name"],inf)
"""
Tile("gazon",fileName="gazon.png",doPass=True)
Tile("vide",fileName="vide.png",doPass=False,speed=0.001)
Tile("eau",fileName="eau.png",doPass=True,speed=0.05,type="map")
Tile("pommier",fileName="Pommier.png",doPass=False,type="surmap")
Tile("arbre",fileName="Arbre de base.png",doPass=False,type="surmap")
Tile("nada",doPass=True,type="surmap")
Tile("sable",fileName="sable.png",doPass=True,speed=0.075,type="map")
Tile("Eau+Sable (NW)",fileName="eaunw.png",doPass=True,speed=0.05,type="map")
Tile("Eau+Sable (NE)",fileName="eaune.png",doPass=True,speed=0.05,type="map")
Tile("Eau+Sable (SW)",fileName="eausw.png",doPass=True,speed=0.05,type="map")
Tile("Eau+Sable (SE)",fileName="eause.png",doPass=True,speed=0.05,type="map")
Tile("sable+Eau (NW)",fileName="sablenw.png",doPass=True,speed=0.075,type="map")
Tile("sable+Eau (NE)",fileName="sablene.png",doPass=True,speed=0.075,type="map")
Tile("sable+Eau (SW)",fileName="sablesw.png",doPass=True,speed=0.075,type="map")
Tile("sable+Eau (SE)",fileName="sablese.png",doPass=True,speed=0.075,type="map")
Tile("Cocotier",fileName="cocotier.png",doPass=False,type="surmap")
Tile("Bananier",fileName="bananier.png",doPass=False,type="surmap")
Tile("Chemin de cailloux NS",fileName="chemincaillou.png",doPass=True,type="surmap")
Tile("Chemin de cailloux WE",fileName="chemincaillouwe.png",doPass=True,type="surmap")
Tile("darkeau",fileName="darkeau.png",doPass=False,type="map")
"""
for i in Tile.tiles:
    print(i.toString())
