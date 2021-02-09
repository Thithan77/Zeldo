#coding:utf-8
import pygame # import de pygame
from pygame.locals import * # import des constantes de Pygame comme QUIT
from classes.bordel import * # On importe la libairie perso bordel (ya des trucs bordels dedans)
import os; # Plein de fonctions sytèmes utiles (geta)
pygame.init() # Initialisation de pygame
pygame.key.set_repeat(10, 16) # set_repeat(délais avant de repêter une touche,délais entre chaque répétition)
import json # On importe la librairie json pour pouvoir utiliser des fichiers au format JSON
from math import *
import classes.player as pl# On importe la classe qui gère le joueur
try:
    options = json.loads(open("config.json",'r').read()) # On importe le fichier json sous forme d'un objet
except:
    print("Erreur dans le chargement du fichier de configuration (existe-t-il ?)")
    sys.exit()
fen = pygame.display.set_mode((options["fen"]["width"], options["fen"]["height"])) # On définit la fenêtre à la taille indiquée dans le fichier config
clock = pygame.time.Clock() # la clock qui permet de gérer les FPS (stonks)
from init import *
font = pygame.font.SysFont(None, 24) # On charge la police d'écriture
playing = True
map = json.loads(open("map.json",'r').read()) # on charge la map depuis le fichier
player = pl.Player() # On initalise le joueur
xspeed,yspeed = 0,0
while playing: # tant que le joueur joue on continue la boucle du jeu
    fen.fill((255,255,255))
    speed = Tile.tiles[map[int(player.x)][int(player.y)]].speed
    for event in pygame.event.get(): # les évènements
        if event.type == pygame.QUIT: # croix rouge
            playing = False
        if event.type == pygame.KEYDOWN: # Touche pressée
            if event.key == K_z:
                yspeed = -1
            if event.key == K_s:
                yspeed = 1
            if event.key == K_q:
                xspeed = -1
            if event.key == K_d:
                xspeed = 1
        if event.type == pygame.KEYUP: # Touche pressée
            speed = Tile.tiles[map[int(player.x)][int(player.y)]].speed
            if event.key == K_z:
                yspeed = 0
            if event.key == K_s:
                yspeed = 0
            if event.key == K_q:
                xspeed = 0
            if event.key == K_d:
                xspeed = 0
    player.x+=xspeed*speed
    player.y+=yspeed*speed
    col = int(options["fen"]["height"]//32+3)
    lin = int(options["fen"]["width"]//32+3)
    xmin = player.x*32-(options["fen"]["width"]/2)+32
    ymin = player.y*32-(options["fen"]["height"]/2)+32
    x = xmin
    y = ymin
    for i in range(col):
        yc = y%32
        for j in range(lin):
            xc = x%32
            if(floor(x/32) <= 0 or floor(y/32) <= 0 or floor(x/32) >= 100 or floor(y/32) >= 100):
                fen.blit(Tile.tiles[Tile.nameToNumber["vide"]].texture,(j*32-xc,i*32-yc))
            else:
                yz = floor(y/32)
                xz = floor(x/32)
                texture = Tile.tiles[map[int(xz-1)][int(yz-1)]].texture
                #texture = Tile.tiles[0].texture
                fen.blit(texture,((j)*32-xc,(i)*32-yc))
            x+=32
        x = xmin
        y+=32
    fen.blit(player.texture,(options["fen"]["width"]/2-16,options["fen"]["height"]/2-16))
    img = font.render('VERSION ALPHA - MMORPG - Projet NSI', True, (255,255,255))
    fen.blit(img, (20, 32))
    img = font.render('PosX: {}'.format(player.x), True, (255,255,255))
    fen.blit(img, (20, 64))
    img = font.render('PosY: {}'.format(player.y), True, (255,255,255))
    fen.blit(img, (20, 96))
    FPS = str(int(clock.get_fps()))
    img = font.render('FPS: {}'.format(FPS), True, (255,255,255))
    fen.blit(img, (20, 128))
    pygame.display.flip()
    #os.system("pause")
    clock.tick(60)
pygame.quit()
