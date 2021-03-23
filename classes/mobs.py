from classes.bordel import *
import pygame
from random import *
from _thread import *
from time import *
import sys
mob_x=10
mob_y=20
def threadmob(Tile,cmap):
	global mob_x, mob_y
	while True:

		deplacement=randint(1,4)
		for i in range(150):

			sleep(1/50)
			if deplacement==1:
				if Tile.tiles[cmap.gs(int(mob_x+0.01+1),int(mob_y))].doPass:
					mob_x+=0.01
			elif deplacement==2:
				if Tile.tiles[cmap.gs(int(mob_x),int(mob_y-0.01))].doPass:
					mob_y-=0.01
			elif deplacement==3:
				if Tile.tiles[cmap.gs(int(mob_x),int(mob_y+0.01+1))].doPass:
					mob_y+=0.01
			else:
				if Tile.tiles[cmap.gs(int(mob_x-0.01),int(mob_y))].doPass:
					mob_x-=0.01

def draw_mobs(fen,player,cmap,Tile,options):
	global mob_x, mob_y
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
	if(sys.platform == "linux"):
		v = pygame.image.load("assets/vache.png").convert_alpha()
	else:
		v = pygame.image.load("assets\\vache.png").convert_alpha()
	v.set_colorkey((255,255,255))

	x,y = globalToLocalCoord(mob_x*32,mob_y*32,player.x,player.y,options)


	fen.blit(v,(x,y))
def start(Tile,cmap):
	start_new_thread(threadmob,(Tile,cmap))
