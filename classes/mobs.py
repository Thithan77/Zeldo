from classes.bordel import *
def draw_mobs(fen,player,cmap,Tile):
    """
    fen = la fenêtre python
    player = l'objet du joueur
    player.x / player.y les coordonnées du joueur
    globalToLocalCoord(x,y,playerx,playery) (x,y): les coordonnées sur la map (playerx,playery):coordonnées du joueur sur la map / renvoit les coordonnées sur l'écran
    var = pygame.image.load("chemin du fichier").convert_alpha() pour charger une texture
    fen.blit(texture,(x,y)) pour blit la texture sur l'écran
    cmap.gm(x,y) Récupérer l'id du tile aux coordonnées x,y
    Tile.tiles[x] Accès à l'objet Tile correspondant à l'id x (voir la doc du fichier Tile.py)
    Si t'as besoin d'autres infos hésite pas à me demander ^^
    """
    pass
