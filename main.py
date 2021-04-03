#coding:utf-8
import pygame # import de pygame
import tkinter # import de tkinter
from pygame.locals import * # import des constantes de Pygame comme QUIT
from classes.bordel import * # On importe la libairie perso bordel (ya des trucs bordels dedans)
import os # Plein de fonctions sytèmes utiles (geta)
import sys # Import de sys
import socket # Socket pour le jeu en ligne
pygame.init() # Initialisation de pygame
#pygame.key.set_repeat(10, 16) # set_repeat(délais avant de repêter une touche,délais entre chaque répétition)
import json # On importe la librairie json pour pouvoir utiliser des fichiers au format JSON
from math import *
import classes.player as pl# On importe la classe qui gère le joueur
import classes.map as cmap # La classe qui gère la map
from functools import partial # Une fonction utile mais flemme d'expliquer pourquoi
import time
import classes.inventories as inventories # La classe qui gère les inventaires
import classes.mobs # Les mobs (c'est géré par Léo je lui fait confiance owo)
id = [0]
try:
    options = json.loads(open("config.json",'r').read()) # On importe le fichier json sous forme d'un objet
except:
    print("Erreur dans le chargement du fichier de configuration (existe-t-il ?)")
    sys.exit()
# Petit launcher pour récupérer les informations de lancement
tk = tkinter.Tk() # On créé la fenêtre tkinter
tkinter.Label(tk,text="MMORPG Launcher").pack()
pseudo = tkinter.StringVar()
tkinter.Entry(tk,textvariable=pseudo).pack()
multi = tkinter.IntVar()
tkinter.Checkbutton(tk, text='Multiplayer',variable=multi).pack()
discord = tkinter.IntVar()
tkinter.Checkbutton(tk, text='Discord Rich Presence',variable=discord).pack()
tk.mainloop()
del tk
fen = pygame.display.set_mode((options["fen"]["width"], options["fen"]["height"]),DOUBLEBUF) # On définit la fenêtre à la taille indiquée dans le fichier config
pygame.display.set_caption("MMORPG")
if(sys.platform == "linux"):
    icon = pygame.image.load("assets/Logo.png")
else:
    icon = pygame.image.load("assets\\Logo.png")
pygame.display.set_icon(icon)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP,MOUSEBUTTONUP,MOUSEBUTTONDOWN]) # On n'active pas tous les évènements pour gagner un peu en performance
clock = pygame.time.Clock() # la clock qui permet de gérer les FPS (stonks)
from init import * # On importe le fichier init ce qui a pour effet de lancer l'initialisation du jeu
if("multiplayer" in sys.argv): # Si multiplayer est dans les argv (Example : le programme est lancé avec "python main.py multiplayer")
    print("Mode multijoueur enclenché")
    map = cmap.multiMap(Tile,sys.argv) # gestion différente de la map qui est importée et actualisée depuis le serveur
else:
    map = cmap.Map(Tile,sys.argv)
classes.mobs.start(Tile,map)
import pypresence
def event_test(a):
    print(f"Yeaaaaaaaah j'ai eu {a} c'est trop cool")
if(discord.get() == 1):
    try:
        dPresence = pypresence.Presence("823840156939190292");
        dPresence.connect()
        dPresence.update(start=time.time(),state="En jeu",details="Pseudo: {}".format(pseudo.get()),large_image="logo",small_image="perso",join="trololololo")
        dClient = pypresence.Client("823840156939190292")
        dClient.start()
        dClient.register_event("ACTIVITY_JOIN", event_test, args={})
    except:
        print("Discord Rich Presence n'a pas pu être chargé.")
font = pygame.font.SysFont(None, 24) # On charge la police d'écriture
playing = True # variable pour la boucle principale du jeu
editor_click = False # grosso modo si le clic est enfoncé ça permet de poser plusieurs cases à la suite
editorActivated = False # Si l'éditeur est activé (C'est pour toi ça Léo)
noclip = False # Le noclip (mode fantôme : tu traverses les murs)
placetick = 0
InventoryTile = it() # Récupération de InventoryTile
player = pl.Player() # On initalise le joueur
xspeed,yspeed = 0,0 # la vitesse du joueur selon les axes x et y
lastTime = time.time() # Pour calculer les performances et tout
tot = 0 # Le temps de jeu
n = 0 # Le nombre de frames
inventory = inventories.Inventory(InventoryTile)
selected_inv = 8 # La case sélectionnée dans l'inventaire
invOpen = False # Si l'inventaire est ouvert
drag = False # Si le joueur est en train de drag un item
drag_x = 0 # le décalage x du drag avec la grille
drag_y = 0 # Le décalage y du drag avec la grille
dragged_Item = None # L'item en cours de drag
dragged_Item_count = 0 # Le nombre d'item en cours de drag
drag_coming_x = 0 # l'origine x dans l'inventaire de l'item draggé
drag_coming_y = 0 # l'origine y dans l'inventaire de l'item draggé
timeBreaking = time.time() # Début du cassage de bloc (ici on le définit à une valeur qui va changer)
breaking = False # Si le joueur est en train de casser
break_x = 0 # La position x de cassage
break_y = 0 # La position y de cassage
if(multi.get() == 1): # Si multiplayer est dans les argv (Example : le programme est lancé avec "python main.py multiplayer")
    print("Mode multijoueur enclenché")
    map = cmap.multiMap(Tile,sys.argv,player,pseudo) # gestion différente de la map qui est importée et actualisée depuis le serveur
else:
    map = cmap.Map(Tile,sys.argv)
while playing: # tant que le joueur joue on continue la boucle du jeu
    lastTime = time.time()
    placetick +=1
    fen.fill((255,255,255)) # On met un fill blanc tout derrière
    speed = Tile.tiles[int(map.gm(int(player.x),int(player.y))//1)].speed # On récupère la vitesse de la case qui va servir de multiplicateur
    for event in pygame.event.get(): # les évènements
        if event.type == pygame.MOUSEBUTTONUP:
            if(event.button == 2): # Si c'est un clic molette
                editor_click = False # On désactive la placement auto des tiles
            if(event.button == 1):
                if(drag): # Drag d'un item dans l'inventaire
                    drag = False
                    x0 = options["fen"]["width"] - 9*32
                    y0 = options["fen"]["height"] - 9*32
                    x,y = pygame.mouse.get_pos()
                    x-=x0
                    y-=y0
                    if(x>0 and y>0):
                        rx = x//32
                        ry = y//32
                        if(inventory.tab[rx][ry].name == "storage"):
                            if(inventory.tab[rx][ry].item == None):
                                inventory.tab[rx][ry].item = dragged_Item
                                inventory.tab[rx][ry].count = dragged_Item_count
                                dragged_Item = None
                            elif(inventory.tab[rx][ry].item == dragged_Item):
                                inventory.tab[rx][ry].count+=dragged_Item_count
                            else:
                                inventory.tab[drag_coming_x][drag_coming_y].item = dragged_Item
                                inventory.tab[drag_coming_x][drag_coming_y].count = dragged_Item_count
                        else:
                            inventory.tab[drag_coming_x][drag_coming_y].count = dragged_Item_count
                    else:
                        inventory.tab[drag_coming_x][drag_coming_y].count = dragged_Item_count
                if(breaking):
                    breaking = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(event.button == 2):
                editor_click = True # On active le placement auto des tiles
            if(event.button == 1 and invOpen):
                x0 = options["fen"]["width"] - 9*32
                y0 = options["fen"]["height"] - 9*32
                x,y = pygame.mouse.get_pos()
                x-=x0
                y-=y0
                if(x>0 and y>0):
                    rx = x//32
                    ry = y//32
                    drag_x = x-rx*32
                    drag_y = y-ry*32
                    if(inventory.tab[rx][ry].name == "storage"):
                        if(inventory.tab[rx][ry].item != None):
                            drag = True
                            dragged_Item = inventory.tab[rx][ry].item
                            dragged_Item_count = inventory.tab[rx][ry].count
                            inventory.tab[rx][ry].item = None
                            inventory.tab[rx][ry].count = 0
                            drag_coming_x = rx
                            drag_coming_y = ry
            elif(event.button == 3 and invOpen):
                x0 = options["fen"]["width"] - 9*32
                y0 = options["fen"]["height"] - 9*32
                x,y = pygame.mouse.get_pos()
                x-=x0
                y-=y0
                if(x>0 and y>0):
                    rx = x//32
                    ry = y//32
                    drag_x = x-rx*32
                    drag_y = y-ry*32
                    if(inventory.tab[rx][ry].name == "storage"):
                        if(inventory.tab[rx][ry].item != None and inventory.tab[rx][ry].count>1):
                            drag = True
                            dragged_Item = inventory.tab[rx][ry].item
                            toTake = inventory.tab[rx][ry].count//2
                            inventory.tab[rx][ry].count-=toTake
                            dragged_Item_count = toTake
                            drag_coming_x = rx
                            drag_coming_y = ry
            elif(event.button == 1):
                breaking = True
                timeBreaking = time.time()
                x,y= pygame.mouse.get_pos()
                x,y = pygame.mouse.get_pos()
                rx = int((x-(options["fen"]["width"]/2)+player.x*32)//32)
                ry = int((y-(options["fen"]["height"]/2)+player.y*32)//32)
                break_x = rx
                break_y = ry
            inv = pygame.Rect(options["fen"]["width"]-32*9,options["fen"]["height"]-32,9*32,32)
            if(inv.collidepoint(pygame.mouse.get_pos())):
                x,y = pygame.mouse.get_pos()
                ux = x-(options["fen"]["width"]-32*9)
                ux//=32
                selected_inv = ux
        if event.type == pygame.QUIT: # croix rouge
            playing = False # On met à False donc la boucle s'arrête et le jeu se ferme
            print(tot/n*1000) # On affiche le temps moyen pour une frame
        if event.type == pygame.KEYDOWN: # Touche pressée
            if event.key == K_z:
                yspeed = -1 # Vers la gauche
            if event.key == K_s:
                yspeed = 1 # vers la droite
            if event.key == K_q:
                xspeed = -1 # Vers le haut
            if event.key == K_d:
                xspeed = 1 # vers le bas
            if event.key == K_k:
                noclip = not noclip # On change l'état du noclip vers l'inverse
            if event.key == K_e:
                invOpen = not invOpen # On ouvre l'inventaire principal en mettant en pause cette fonction
            if event.key == K_g: # Sauvegarde de la carte
                jzon = open("map.json",'w') # On charge le fichier map
                conversion = [] # Pas utile d'expliquer mais on convertit si les tiles ont changées
                for i in Tile.tiles:
                    g = {} # variable temporaire
                    g["name"] = i.name
                    g["id"] = i.id
                    conversion.append(g)
                maps = [conversion,map.map,map.surmap]
                jzon.write(json.dumps(maps))
                print("Saved !")
            if event.key == K_o: # Pour tourner une tile compatible (Attention provoque un crash si pas déclarée comme tournable)
                if(editorActivated):
                    x,y = pygame.mouse.get_pos()
                    rx = (x-(options["fen"]["width"]/2)+player.x*32)//32
                    ry = (y-(options["fen"]["height"]/2)+player.y*32)//32
                    rot = int(map.gm(int(rx),int(ry))%1*10)
                    print(rot+1)
                    if(rot == 3):
                        map.modify(int(rx),int(ry),map.gm(int(rx),int(ry)) - 0.3)
                    else:
                        map.modify(int(rx),int(ry),map.gm(int(rx),int(ry)) + 0.1)
            if event.key == K_y: # Ouvre le menu tkinter pour l'éditeur
                editorActivated = True
                tk = tkinter.Tk()
                page = 0
                for j in Tile.tiles[:10]:
                    bouton = tkinter.Button(tk,text=j.name,command=partial(editor,j.id,tk,id))
                    bouton.pack()
                tkinter.Button(tk,text="Page suivante",command=partial(next,tk,page,Tile.tiles,id)).pack()
                tkinter.Button(tk,text="Page précédente",command=partial(past,tk,page,Tile.tiles,id)).pack()
                tk.mainloop()
            if event.key == K_j:
                tk = tkinter.Tk()
                tkinter.Button(tk,text="New Game",command=partial(join,tk,"newGame",map)).pack()
                gamen = tkinter.StringVar()
                tkinter.Entry(tk,textvariable=gamen).pack()
                tkinter.Button(tk,text="Join",command=partial(join,tk,gamen,map)).pack()
                tk.mainloop()
            if event.key == K_r:
                for i,j in enumerate(Tile.tiles):
                    if(j.fileName):
                        if(sys.platform == "linux"):
                            j.texture2 = pygame.image.load("assets/"+j.fileName).convert_alpha()
                        else:
                            j.texture2 = pygame.image.load("assets\\"+j.fileName).convert_alpha()
                        j.texture2.set_colorkey((255,255,255))
                        j.texture = pygame.Surface((32,32)).convert_alpha()
                        j.texture.fill((0,0,0,0))
                        j.texture.blit(j.texture2,(0,0,32,32))
                        Tile.tiles[i] = j
        if event.type == pygame.KEYUP: # Touche pressée
            speed = Tile.tiles[int(map.gm(int(player.x),int(player.y))//1)].speed
            if event.key == K_z:
                yspeed = 0
            if event.key == K_s:
                yspeed = 0
            if event.key == K_q:
                xspeed = 0
            if event.key == K_d:
                xspeed = 0
    if(noclip):
        player.x+=xspeed*speed
        player.y+=yspeed*speed
        #print(Tile.tiles[map[int((player.x*32+10)//32)][int(floor(player.y))]].doPass,Tile.tiles[surmap[int((player.x*32+10)//32)][int(floor(player.y))]].doPass)
    else:
        if(xspeed == 1 and Tile.tiles[int(map.gs(int((player.x*32+10)//32),int(floor(player.y)))//1)].doPass and Tile.tiles[int(map.gm(int((player.x*32+10)//32),int(floor(player.y)))//1)].doPass):
            player.x+=xspeed*speed
        if(xspeed == -1 and Tile.tiles[int(map.gs(int((player.x*32-10)//32),int(floor(player.y)))//1)].doPass and Tile.tiles[int(map.gm(int((player.x*32-10)//32),int(floor(player.y)))//1)].doPass):
            player.x+=xspeed*speed
        if(yspeed == 1 and Tile.tiles[int(map.gs(int(floor(player.x)),int((player.y*32+10)//32))//1)].doPass and Tile.tiles[int(map.gm(int(floor(player.x)),int((player.y*32+10)//32))//1)].doPass):
            player.y+=yspeed*speed
        if(yspeed == -1 and Tile.tiles[int(map.gs(int(floor(player.x)),int((player.y*32-10)//32))//1)].doPass and Tile.tiles[int(map.gm(int(floor(player.x)),int((player.y*32-10)//32))//1)].doPass):
            player.y+=yspeed*speed
    if(editorActivated and editor_click):
        x,y = pygame.mouse.get_pos()
        rx = (x-(options["fen"]["width"]/2)+player.x*32)//32
        ry = (y-(options["fen"]["height"]/2)+player.y*32)//32
        if(Tile.tiles[id[0]].type == "surmap"):
            map.surmodify(int(rx),int(ry),id[0])
        else:
            map.modify(int(rx),int(ry),id[0])
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
                if(map.gm(int(xz-1),int(yz-1))%1 == 0):
                    case = Tile.tiles[map.gm(int(xz-1),int(yz-1))]
                    if(case.multiTile):
                        xy = int(yz+xz)
                        texture = case.textures[xy%len(case.textures)]
                        texture = texture[0]
                    else:
                        texture = case.texture
                    fen.blit(texture,((j)*32-xc,(i)*32-yc))
                else:
                    rot = int(map.gm(int(xz-1),int(yz-1))%1*10)
                    #print(rot)
                    case = Tile.tiles[int(map.gm(int(xz-1),int(yz-1))//1)]
                    if(case.multiTile):
                        xy = int(yz+xz)
                        texture = case.textures[xy%len(case.textures)][rot]
                    else:
                        try:
                            texture = case.textures[rot]
                        except AttributeError:
                            texture = Tile.tiles[0].texture
                    fen.blit(texture,((j)*32-xc,(i)*32-yc))
                if(Tile.tiles[map.gs(int(xz-1),int(yz-1))].name != "nada"):
                    try:
                        texture = Tile.tiles[map.gs(int(xz-1),int(yz-1))].texture
                    except AttributeError:
                        texture = Tile.tiles[0].texture
                    fen.blit(texture,((j)*32-xc,(i)*32-yc))
            x+=32
        x = xmin
        y+=32
    fen.blit(player.texture,(options["fen"]["width"]/2-16,options["fen"]["height"]/2-16))
    map.draw_others(fen,player,options)
    for i in range(9):
        texture = inventory.tab[i][8].get_texture()
        if(i == selected_inv):
            s = pygame.Surface((32,32)).convert_alpha()
            s.fill((255,0,0,100))
            texture.blit(s,(0,0))
        fen.blit(texture,(options["fen"]["width"]-32*9+32*i,options["fen"]["height"]-32))
    if(invOpen):
        for i in range(9):
            for j in range(9):
                xl = i*32
                yl = j*32
                x = options["fen"]["width"] - 9*32 + xl
                y = options["fen"]["height"] - 9*32 + yl
                fen.blit(inventory.tab[i][j].get_texture(),(x,y))
        if(drag):
            texture = Item.items[Item.nameToNumber[dragged_Item]].texture
            x,y = pygame.mouse.get_pos()
            x = x-drag_x
            y = y-drag_y
            fen.blit(texture,(x,y))
    if(breaking):
        delta = time.time()-timeBreaking
        r = int(delta/4*255)
        if(delta >=4):
            timeBreaking = time.time()
            r = 0
            dropped = Tile.tiles[map.gs(break_x,break_y)].drop
            if(dropped != None):
                print(type(dropped) == type([]))
                if(type(dropped) == type([])):
                    for i in dropped:
                        inventory.add(i,1)
                else:
                    inventory.add(dropped,1)
            map.surmodify(break_x, break_y, Tile.nameToNumber["nada"])
        x = break_x*32-player.x*32+options["fen"]["width"]/2
        y = break_y*32-player.y*32+options["fen"]["height"]/2
        s = pygame.Surface((32,32)).convert_alpha()
        s.fill((r,0,0,100))
        fen.blit(s,(x,y))
    classes.mobs.draw_mobs(fen,player,cmap,Tile,options)
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
    tot += (time.time() - lastTime)
    n+= 1
    clock.tick(60)
pygame.quit()
