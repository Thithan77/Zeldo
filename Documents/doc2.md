# NOTE DE CADRAGE

## Description de l’équipe et rôle de chacun
Les rôles ne sont pas vraiment définis , chacun peut s’intéresser à plusieurs parties du projet
- Léo : Mapping
- Loïc : Graphisme
- Thibaut : Programmation / son
- Julien (groupe B2) : Graphisme / Code
## Espace Numérique de Travail ENT
Utilisation d'une repository Github privée
- assets : Les fichiers .png qui sont les textures du jeu
- classes
  - bordel.py : Fonctions diverses
  - map.py : Gestion de la map
  - player.py : Gestion du personnage
  - Tile.py : Classe Tile
  - InventoryTile.py : Classe InventoryTile
  - Item.py : Classe Item
  - inventories.py : Gestion des inventaires / Classe Inventory
- content
  - inventories
    - layout : Les layouts pour les inventaires (en dévellopement / sujet à changement prochainement)
    - python : gestion des inventaires mais en python (en dévellopement / sujet à changement prochainement)
  - tiles : Fichiers .yml qui sont utilisés pour tous les tiles du jeu
  - items : Idem pour les items
- Documents : Contient les documents dont celui-ci
- server : Dossier qui contient le fichier server.py qui permet d'héberger un serveur (en dévellopement / sujet à changement prochainement)
- build.py : Test d'utilisation d'une librairie pour utiliser python en stand-alone (pour la diffusion du jeu)
- config.json : La configuration du jeu (actuellement uniquement la résolution mais sujet à différents ajouts)
- init.py : Chargement du jeu en particulier de tous les fichiers .yml (voir doc3 pour plus d'information sur le fonctionnement)
- main.py : Le fichier principal du jeu
- map.json : Stockage de la carte / Format temporaire car plus simple à modifier manuellement un module comme Pickle sera peut être utilisé plus tard
- Objectifs.md : Les objectifs (inutile)
- perlinNoise.py : test de la génération en utilisant le bruit de Perlin
