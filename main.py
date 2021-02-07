#coding:utf-8
import pygame # import de pygame
from pygame.locals import * # import des constantes de Pygame comme QUIT
from classes.bordel import * # On importe la libairie perso bordel (ya des trucs bordels dedans)
import sys; # Plein de fonctions sytèmes utiles (geta)
pygame.init() # Initialisation de pygame
pygame.key.set_repeat(10, 16) # set_repeat(délais avant de repêter une touche,délais entre chaque répétition)
import json # On importe la librairie json pour pouvoir utiliser des fichiers au format JSON
import classes.player as pl# On importe la classe qui gère le joueur
try:
    options = json.loads(open("config.json",'r').read()) # On importe le fichier json sous forme d'un objet
except:
    print("Erreur dans le chargement du fichier de configuration (existe-t-il ?)")
    sys.exit()
fen = pygame.display.set_mode((options["fen"]["width"], options["fen"]["height"])) # On définit la fenêtre à la taille indiquée dans le fichier config
clock = pygame.time.Clock() # la clock qui permet de gérer les FPS (stonks)
from init import *
font = pygame.font.SysFont(None, 24)
playing = True
map = [[0]*50]*50 # Map de test
player = pl.Player() # On initalise le joueur
while playing:
    fen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_z:
                player.y-=0.1
            if event.key == K_s:
                player.y+=0.1
            if event.key == K_q:
                player.x-=0.1
            if event.key == K_d:
                player.x+=0.1
    col = int(options["fen"]["height"]//32+2)
    lin = int(options["fen"]["width"]//32+2)
    x0 = player.x*32-options["fen"]["width"]
    y0 = player.y*32-options["fen"]["height"]
    x = x0
    y = y0
    for i in range(col):
        yc = y%32 # Le décalage entre le joueur et le quadrillage
        for j in range(lin):
            xc = x%32 # Le décalage entre le joueur et le quadrillage
            xr = x+options["fen"]["width"]/2-xc
            yr = y+options["fen"]["height"]/2-yc
            if(xr//32+1 < 0 or yr//32+1<0):
                fen.blit(Tile.tiles[Tile.nameToNumber["vide"]].texture,(j*32-xc,i*32-yc,32,32))
            else:
                fen.blit(Tile.tiles[map[int(xr//32)][int(yr//32)]].texture,(j*32-xc,i*32-yc,32,32))
            x+=32
        y+=32
        x = x0
    pygame.draw.rect(fen,(255,0,0),(options["fen"]["width"]/2-12,options["fen"]["height"]/2-12,24,24))
    img = font.render('PosX: {}'.format(player.x), True, (255,255,255))
    fen.blit(img, (20, 32))
    img = font.render('PosY: {}'.format(player.y), True, (255,255,255))
    fen.blit(img, (20, 64))
    FPS = str(int(clock.get_fps()))
    img = font.render('FPS: {}'.format(FPS), True, (255,255,255))
    fen.blit(img, (20, 96))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
