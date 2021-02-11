from classes.Tile import *
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
Tile("Chemin de cailloux",fileName="chemincaillou.png",doPass=True,type="surmap")