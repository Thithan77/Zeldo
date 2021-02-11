#coding:utf-8
import pygame # import de pygame
import tkinter
from pygame.locals import * # import des constantes de Pygame comme QUIT
from classes.bordel import * # On importe la libairie perso bordel (ya des trucs bordels dedans)
import os; # Plein de fonctions sytèmes utiles (geta)
pygame.init() # Initialisation de pygame
#pygame.key.set_repeat(10, 16) # set_repeat(délais avant de repêter une touche,délais entre chaque répétition)
import json # On importe la librairie json pour pouvoir utiliser des fichiers au format JSON
from math import *
import classes.player as pl# On importe la classe qui gère le joueur
from functools import partial
id = [0]
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
editor_click = False
editorActivated = False
"""
map = []
for i in range(200):
    map.append([])
    for j in range(200):
        map[i].append(0)
surmap = []
for i in range(200):
    surmap.append([])
    for j in range(200):
        surmap[i].append(5)
jzon = open("map.json",'w')
maps = [map,surmap]
jzon.write(json.dumps(maps))
print("Saved !")
"""
map,surmap = json.loads(open("map.json",'r').read()) # on charge la map depuis le fichier
player = pl.Player() # On initalise le joueur
xspeed,yspeed = 0,0
while playing: # tant que le joueur joue on continue la boucle du jeu
    fen.fill((255,255,255))
    speed = Tile.tiles[map[int(player.x)][int(player.y)]].speed
    for event in pygame.event.get(): # les évènements
        if event.type == pygame.MOUSEBUTTONUP:
            if(event.button == 2):
                editor_click = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(event.button == 2):
                editor_click = True
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
            if event.key == K_g:
                jzon = open("map.json",'w')
                maps = [map,surmap]
                jzon.write(json.dumps(maps))
                print("Saved !")
            if event.key == K_y:
                editorActivated = True
                tk = tkinter.Tk()
                page = 0
                for j in Tile.tiles[:10]:
                    bouton = tkinter.Button(tk,text=j.name,command=partial(editor,j.id,tk,id))
                    bouton.pack()
                tkinter.Button(tk,text="Page suivante",command=partial(next,tk,page,Tile.tiles,id)).pack()
                tkinter.Button(tk,text="Page précédente",command=partial(past,tk,page,Tile.tiles,id)).pack()
                tk.mainloop()
            if event.key == K_r:
                for i,j in enumerate(Tile.tiles):
                    if(j.fileName):
                        j.texture2 = pygame.image.load("assets\\"+j.fileName).convert_alpha()
                        j.texture2.set_colorkey((255,255,255))
                        j.texture = pygame.Surface((32,32)).convert_alpha()
                        j.texture.fill((0,0,0,0))
                        j.texture.blit(j.texture2,(0,0,32,32))
                        Tile.tiles[i] = j
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
    if(xspeed == 1 and Tile.tiles[surmap[int((player.x*32+10)//32)][int(floor(player.y))]].doPass and Tile.tiles[map[int((player.x*32+10)//32)][int(floor(player.y))]].doPass):
        player.x+=xspeed*speed
    if(xspeed == -1 and Tile.tiles[surmap[int((player.x*32-10)//32)][int(floor(player.y))]].doPass and Tile.tiles[map[int((player.x*32-10)//32)][int(floor(player.y))]].doPass):
        player.x+=xspeed*speed
    if(yspeed == 1 and Tile.tiles[surmap[int(floor(player.x))][int((player.y*32+10)//32)]].doPass and Tile.tiles[map[int(floor(player.x))][int((player.y*32+10)//32)]].doPass):
        player.y+=yspeed*speed
    if(yspeed == -1 and Tile.tiles[surmap[int(floor(player.x))][int((player.y*32-10)//32)]].doPass and Tile.tiles[map[int(floor(player.x))][int((player.y*32-10)//32)]].doPass):
        player.y+=yspeed*speed
    if(editorActivated and editor_click):
        x,y = pygame.mouse.get_pos()
        rx = (x-(options["fen"]["width"]/2)+player.x*32)//32
        ry = (y-(options["fen"]["height"]/2)+player.y*32)//32
        if(Tile.tiles[id[0]].type == "surmap"):
            surmap[int(rx)][int(ry)] = id[0]
        else:
            map[int(rx)][int(ry)] = id[0]
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
            if(floor(x/32) <= 0 or floor(y/32) <= 0 or floor(x/32) >= 200 or floor(y/32) >= 200):
                fen.blit(Tile.tiles[Tile.nameToNumber["darkeau"]].texture,(j*32-xc,i*32-yc))
            else:
                yz = floor(y/32)
                xz = floor(x/32)
                texture = Tile.tiles[map[int(xz-1)][int(yz-1)]].texture
                fen.blit(texture,((j)*32-xc,(i)*32-yc))
                if(Tile.tiles[surmap[int(xz-1)][int(yz-1)]].name != "nada"):
                    texture = Tile.tiles[surmap[int(xz-1)][int(yz-1)]].texture
                    fen.blit(texture,((j)*32-xc,(i)*32-yc))
            x+=32
        x = xmin
        y+=32
    fen.blit(player.texture,(options["fen"]["width"]/2-16,options["fen"]["height"]/2-16))
    img = font.render('VERSION ALPHA - MMORPG + EDITOR - Projet NSI', True, (255,255,255))
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
