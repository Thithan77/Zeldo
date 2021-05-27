from classes.bordel import *
import pygame
from random import *
from _thread import *
from time import *
import sys

#vache
mob_x=38.7
mob_y=17.8
def threadvache(Tile,cmap):
	global mob_x, mob_y, deplacement
	
	while True:
		
		deplacement=randint(1,19)
		for i in range(150):

			sleep(1/50)
			if deplacement==1:
				if Tile.tiles[cmap.gs(int(mob_x+0.01+1),int(mob_y+0.5))].doPass:
					mob_x+=0.01
				else:
					break
			elif deplacement==2:
				if Tile.tiles[cmap.gs(int(mob_x+0.5),int(mob_y-0.01))].doPass:
					mob_y-=0.01
				else:
					break
			elif deplacement==3:
				if Tile.tiles[cmap.gs(int(mob_x),int(mob_y+0.01+1))].doPass:
					mob_y+=0.01
				else:
					break
			elif deplacement==4:
				if Tile.tiles[cmap.gs(int(mob_x-0.01),int(mob_y+0.5))].doPass:
					mob_x-=0.01
				else:
					break
			elif deplacement==5:
				if Tile.tiles[cmap.gs(int(mob_x+1.01),int(mob_y+1.01))].doPass:
					mob_y+=0.01
					mob_x+=0.01
				else:
					break
			elif deplacement==6:
				if Tile.tiles[cmap.gs(int(mob_x+1.01),int(mob_y-0.01))].doPass:
					mob_y-=0.01
					mob_x+=0.01
				else:
					break
			elif deplacement==7:
				if Tile.tiles[cmap.gs(int(mob_x-0.01),int(mob_y-0.01))].doPass:
					mob_y-=0.01
					mob_x-=0.01
				else:
					break
			elif deplacement==8:
				if Tile.tiles[cmap.gs(int(mob_x-0.01),int(mob_y+1.01))].doPass:
					mob_y+=0.01
					mob_x-=0.01
				else:
					break

def draw_vache(fen,player,cmap,Tile,options):
	global mob_x, mob_y, v, deplacement
	if deplacement==1:
		v = pygame.image.load("assets/vache.png").convert_alpha()
	elif deplacement==5:
		v = pygame.image.load("assets/vache.png").convert_alpha()
	elif deplacement==6:
		v = pygame.image.load("assets/vache.png").convert_alpha()
	elif deplacement==4:
		v= pygame.image.load("assets/vachegauche.png").convert_alpha()
	elif deplacement==7:
		v= pygame.image.load("assets/vachegauche.png").convert_alpha()
	elif deplacement==8:
		v= pygame.image.load("assets/vachegauche.png").convert_alpha()
	elif deplacement==2:
		v= pygame.image.load("assets/vachehaut.png").convert_alpha()
	elif deplacement==3:
		v= pygame.image.load("assets/vachebas.png").convert_alpha()
	elif deplacement==9 or deplacement==10:
		v=pygame.image.load("assets/vache qui broute.png").convert_alpha()
	else:
		v = pygame.image.load("assets/vache.png").convert_alpha()
		
	v.set_colorkey((255,255,255))
	x,y = globalToLocalCoord(mob_x*32,mob_y*32,player.x,player.y,options)


	fen.blit(v,(x,y))
def start(Tile,cmap):
	start_new_thread(threadvache,(Tile,cmap))

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


