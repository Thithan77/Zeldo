#coding:utf-8
# In memorian Mr Ramaholiarison
import sys # Import de sys
import time
"""
logFile = open(f"logs/{time.time()}.log","a")
sys.stdout = logFile
logFileError = open(f"logs/{time.time()}.error.log","a")
sys.stderr = logFileError
"""
import pygame # import de pygame
import tkinter # import de tkinter
from pygame.locals import * # import des constantes de Pygame comme QUIT
from classes.bordel import * # On importe la libairie perso bordel (ya des trucs bordels dedans)
perfReport("preLaunchergameLoading")
import os # Plein de fonctions sytèmes utiles (geta)
import socket # Socket pour le jeu en ligne
pygame.init() # Initialisation de pygame
#pygame.key.set_repeat(10, 16) # set_repeat(délais avant de repêter une touche,délais entre chaque répétition)
import json # On importe la librairie json pour pouvoir utiliser des fichiers au format JSON
from math import *
import classes.player as pl# On importe la classe qui gère le joueur
import classes.map as cmap # La classe qui gère la map
from functools import partial # Une fonction utile mais flemme d'expliquer pourquoi
import classes.inventories as inventories # La classe qui gère les inventaires
import classes.mobs # Les mobs (c'est géré par Léo je lui fait confiance owo)
import classes.fight as fight #Le système de combat (c'est géré par Loïc OwO)
id = [0]
try:
    options = json.loads(open("config.json",'r').read()) # On importe le fichier json sous forme d'un objet
except:
    print("Erreur dans le chargement du fichier de configuration (existe-t-il ?)")
    sys.exit()
# Petit launcher pour récupérer les informations de lancement

tk = tkinter.Tk() # On créé la fenêtre tkinter
tkinter.Label(tk,text="Zeldo Launcher").pack()
pseudo = tkinter.StringVar()
pseudolabel = tkinter.LabelFrame(tk,text="Pseudo")
tkinter.Entry(pseudolabel,textvariable=pseudo).pack()
pseudolabel.pack()
mapNom = tkinter.StringVar()
mapnomlabel = tkinter.LabelFrame(tk,text="Map")
tkinter.Spinbox(mapnomlabel,textvariable=mapNom,values=os.listdir("maps/")).pack()
#tkinter.Entry(mapnomlabel,textvariable=mapNom).pack()
mapnomlabel.pack()
multilabel = tkinter.LabelFrame(tk,text="Multijoueur")
multi = tkinter.IntVar()
def hideMulti():
    if(multi.get() == 1):
        serverlabel.pack()
    else:
        serverlabel.pack_forget()
tkinter.Checkbutton(multilabel, text='Multiplayer',variable=multi,command=hideMulti).pack()
multilabel.pack()
serverlabel = tkinter.LabelFrame(multilabel,text="IP serveur")
serverinfo = tkinter.StringVar()
tkinter.Entry(serverlabel,textvariable=serverinfo).pack()

discord = tkinter.IntVar()
tkinter.Checkbutton(tk, text='Discord Rich Presence',variable=discord).pack()
perfReportEnd("preLaunchergameLoading")
tk.mainloop()
del tk
perfReport("gameLoading")
fen = pygame.display.set_mode((options["fen"]["width"], options["fen"]["height"]),DOUBLEBUF | RESIZABLE) # On définit la fenêtre à la taille indiquée dans le fichier config
pygame.display.set_caption("Zeldo")
if(sys.platform == "linux"):
    icon = pygame.image.load("assets/Logo.png") # le logo du jeu
    light = pygame.image.load("assets/circle.png")
else:
    icon = pygame.image.load("assets\\Logo.png")
    light = pygame.image.load("assets\\circle.png")

pygame.display.set_icon(icon)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP,MOUSEBUTTONUP,MOUSEBUTTONDOWN]) # On n'active pas tous les évènements pour gagner un peu en performance
clock = pygame.time.Clock() # la clock qui permet de gérer les FPS (stonks)
from init import * # On importe le fichier init ce qui a pour effet de lancer l'initialisation du jeu
"""if("multiplayer" in sys.argv): # Si multiplayer est dans les argv (Example : le programme est lancé avec "python main.py multiplayer")
    print("Mode multijoueur enclenché")
    map = cmap.multiMap(Tile,sys.argv) # gestion différente de la map qui est importée et actualisée depuis le serveur
else:
    map = cmap.Map(Tile,sys.argv)
classes.mobs.start(Tile,map)"""
import pypresence # Le module qui gère l'interaction avec Discord
def event_test(a): # Event quand on clique sur "rejoindre" sur Discord (non utilisé)
    print(f"Yeaaaaaaaah j'ai eu {a} c'est trop cool")
if(discord.get() == 1): # Si la case Discord est cochée
    try:
        dPresence = pypresence.Presence("823840156939190292");
        dPresence.connect()
        if(multi.get() == 1): # Si le multijoueur est coché
            dPresence.update(start=time.time(),state="Dans une partie multijoueur",details="Pseudo: {}".format(pseudo.get()),large_image="logo",small_image="perso",party_id="ensah",join="mamamia")
        else:
            dPresence.update(start=time.time(),state=f"En solo sur map {mapNom.get()}",details="Pseudo: {}".format(pseudo.get()),large_image="logo",small_image="perso")
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
day_tick = 0 # Pour définir le jour et la nuit en comptant les ticks
going = 1 # à 1 le temps augmente à -1 il diminue
facing = "south" # De quel côté le personnage regarde
openinvs = [] # liste des inventaires ouverts
zoom = 1.0
debug = False
lastWalk = time.time()
maxFPSInt = 60
chatOpen = False
chatString = ""
varToBordel(options,player)
if(multi.get() == 1): # Si multiplayer est dans les argv (Example : le programme est lancé avec "python main.py multiplayer")
    print(f"Mode multijoueur enclenché ip : {serverinfo.get()}")
    map = cmap.NewMultiMap(Tile,sys.argv,serverinfo.get(),player,pseudo) # gestion différente de la map qui est importée et actualisée depuis le serveur
else:
    map = cmap.NewMap(Tile,sys.argv,mapNom.get())
perfReportEnd("gameLoading")
while playing: # tant que le joueur joue on continue la boucle du jeu
    perfReport("frame")
    lastTime = time.time()
    placetick +=1
    day_tick += going
    if(day_tick == 0 or day_tick == 36000): # Si le temps de la journée atteint 36000 on repart en sens inverse
        going = -going # going est défini à son inverse
    fen.fill((255,255,255)) # On met un fill blanc tout derrière
    speed = Tile.tiles[int(map.gm(int(player.x),int(player.y))//1)].speed # On récupère la vitesse de la case qui va servir de multiplicateur
    perfReport("events")
    for event in pygame.event.get(): # les évènements
        if event.type == pygame.MOUSEBUTTONUP:
            if(event.button == 2): # Si c'est un clic molette
                editor_click = False # On désactive la placement auto des tiles
            if(event.button == 1):
                if(breaking):
                    breaking = False
        if(event.type == MOUSEWHEEL):
            #pass
            zoom += event.y/20
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(event.button == 1):
                dropped_this_tick = False
                if(drag): # Drag d'un item dans l'inventaire
                    drag = False
                    x0 = options["fen"]["width"] - 9*32 # On calcule la position en haut à gauche de l'inventaire
                    y0 = options["fen"]["height"] - 9*32
                    x,y = pygame.mouse.get_pos() # On récupère la position de la souris
                    x-=x0 # On calcule la position sur le référentiel de l'inventaire (en partant du coin)
                    y-=y0
                    if(x>0 and y>0): # Si le clic est sur l'inventaire
                        rx = x//32 # On regarde sur quelle case est le clic
                        ry = y//32
                        if(inventory.tab[rx][ry].acceptItem): # Si on peut rajouter un item sur la case
                            if(inventory.tab[rx][ry].item == None): # Si il n'y a pas d'item dans la case
                                inventory.tab[rx][ry].item = dragged_Item # On définit à l'item qui est drag
                                inventory.tab[rx][ry].count = dragged_Item_count
                                dragged_Item = None
                            elif(inventory.tab[rx][ry].item == dragged_Item): # Si c'est le même item
                                inventory.tab[rx][ry].count+=dragged_Item_count # On ajoute le nombre qu'on a drag
                            else: # Si on ne peut pas rajouter dans la case
                                inventory.tab[drag_coming_x][drag_coming_y].item = dragged_Item # On renvoit à la case d'origine
                                inventory.tab[drag_coming_x][drag_coming_y].count = dragged_Item_count
                                dragged_Item = None
                        else:
                            inventory.tab[drag_coming_x][drag_coming_y].item = dragged_Item # On renvoit à la case d'origine
                            inventory.tab[drag_coming_x][drag_coming_y].count = dragged_Item_count
                            dragged_Item = None
                    else:
                        # Ici on va check si l'item peut pas être rajouté dans un des inventaires ouverts sur la map
                        x,y = pygame.mouse.get_pos() # On récupère la position de la souris
                        for i in openinvs:
                            for k in range(5):
                                for j in range(5):
                                    Xitem = (i["x"]+0.5)*32 + k*32 - player.x*32 + options["fen"]["width"]/2
                                    Yitem = (i["y"]+0.5)*32 + j*32 - player.y*32 + options["fen"]["height"]/2
                                    if(x >= Xitem and x <= Xitem + 32 and y >= Yitem and y <= Yitem + 32):
                                        print(f"oe ça tombe dans l'inventaire case {k};{j}")
                                        dropped_this_tick = True;
                                        if(i["class"].tab[k][j].acceptItem):
                                            if(i["class"].tab[k][j].item == None): # Si il n'y a pas d'item dans la case
                                                i["class"].tab[k][j].item = dragged_Item # On définit à l'item qui est drag
                                                i["class"].tab[k][j].count = dragged_Item_count
                                                dragged_Item = None
                                                dragged_Item_count = 0
                                            elif(i["class"].tab[k][j].item == dragged_Item): # Si c'est le même item
                                                i["class"].tab[k][j].count+=dragged_Item_count # On ajoute le nombre qu'on a drag
                                                dragged_Item = None
                                                dragged_Item_count = 0
                                            else: # Si on ne peut pas rajouter dans la case
                                                inventory.tab[drag_coming_x][drag_coming_y].item = dragged_Item # On renvoit à la case d'origine
                                                inventory.tab[drag_coming_x][drag_coming_y].count = dragged_Item_count
                                                dragged_Item = None
                                                dragged_Item_count = 0
                        if(not dropped_this_tick):
                            x,y = pygame.mouse.get_pos()
                            rx = int((x-(options["fen"]["width"]/2)+player.x*32)//32)
                            ry = int((y-(options["fen"]["height"]/2)+player.y*32)//32)
                            blockapose = Item.items[Item.nameToNumber[dragged_Item]].blockpose
                            if(blockapose != ""):
                                if(Tile.tiles[Tile.nameToNumber[blockapose]].type == "surmap" and Tile.tiles[int(map.gs(rx,ry))].name == "nada"):
                                    map.surmodify(rx,ry,Tile.nameToNumber[blockapose])
                                    if(dragged_Item_count == 1):
                                        dragged_Item_count = 0
                                        dragged_Item = None
                                    else:
                                        dragged_Item_count-=1
                                        drag = True
                                else:
                                    inventory.tab[drag_coming_x][drag_coming_y].item = dragged_Item # On renvoit à la case d'origine
                                    inventory.tab[drag_coming_x][drag_coming_y].count = dragged_Item_count
                                    dragged_Item = None
                                    dragged_Item_count = 0
                            else:
                                inventory.tab[drag_coming_x][drag_coming_y].item = dragged_Item # On renvoit à la case d'origine
                                inventory.tab[drag_coming_x][drag_coming_y].count = dragged_Item_count
                                dragged_Item = None
                                dragged_Item_count = 0
                elif(invOpen):
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
                        if(inventory.tab[rx][ry].acceptItem):
                            if(inventory.tab[rx][ry].item != None):
                                drag = True
                                dragged_Item = inventory.tab[rx][ry].item
                                dragged_Item_count = inventory.tab[rx][ry].count
                                inventory.tab[rx][ry].item = None
                                inventory.tab[rx][ry].count = 0
                                drag_coming_x = rx
                                drag_coming_y = ry
                x,y = pygame.mouse.get_pos()
                if(not dropped_this_tick):
                    for i in openinvs:
                            for k in range(5):
                                for j in range(5):
                                    Xitem = (i["x"]+0.5)*32 + k*32 - player.x*32 + options["fen"]["width"]/2
                                    Yitem = (i["y"]+0.5)*32 + j*32 - player.y*32 + options["fen"]["height"]/2
                                    if(x >= Xitem and x <= Xitem + 32 and y >= Yitem and y <= Yitem + 32):
                                        print(f"oe ça tombe dans l'inventaire case {k};{j}")
                                        if(i["class"].tab[k][j].acceptItem):
                                            drag_x = x-Xitem
                                            drag_y = y-Yitem
                                            if(i["class"].tab[k][j].item != None):
                                                drag = True
                                                dragged_Item = i["class"].tab[k][j].item
                                                dragged_Item_count = i["class"].tab[k][j].count
                                                i["class"].tab[k][j].item = None
                                                i["class"].tab[k][j].count = 0
                                                drag_coming_x = 0 # CORRIGER CA SVP
                                                drag_coming_y = 0
            if(event.button == 2):
                editor_click = True # On active le placement auto des tiles
            if(event.button == 1 and invOpen): # Similaire voir au dessus
                pass
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
                    if(inventory.tab[rx][ry].acceptItem):
                        if(inventory.tab[rx][ry].item != None and inventory.tab[rx][ry].count>1):
                            drag = True
                            dragged_Item = inventory.tab[rx][ry].item
                            toTake = inventory.tab[rx][ry].count//2
                            inventory.tab[rx][ry].count-=toTake
                            dragged_Item_count = toTake
                            drag_coming_x = rx
                            drag_coming_y = ry
            elif(event.button == 1):
                x,y= pygame.mouse.get_pos()
                rx = int((x-(options["fen"]["width"]/2)+player.x*32)//32)
                ry = int((y-(options["fen"]["height"]/2)+player.y*32)//32)
                if(Tile.tiles[int(map.gs(rx,ry))].openinvtxt == ""):
                    break_x = rx
                    break_y = ry
                    breaking = True
                    timeBreaking = time.time()
                else:
                    alreadyopen = False
                    index = 0
                    for i in openinvs:
                        if(i["x"] == rx and i["y"] == ry):
                            alreadyopen = True
                            openatindex = index
                        index+=1
                    state = map.getStateObject("map",rx,ry)
                    if(not alreadyopen):
                        if("storage" in state):
                            #newinv = state["storage"]
                            newinv = {}
                            newinv["x"] = rx
                            newinv["y"] = ry
                            newinv["class"] = Tile.tiles[int(map.gs(rx,ry))].openinv(InventoryTile)
                            for i in range(len(state["storage"])):
                                for j in range(len(state["storage"][i])):
                                    newinv["class"].tab[i][j].item = state["storage"][i][j]["item"]
                                    newinv["class"].tab[i][j].count = state["storage"][i][j]["count"]
                        else:
                            newinv = {}
                            newinv["x"] = rx
                            newinv["y"] = ry
                            newinv["class"] = Tile.tiles[int(map.gs(rx,ry))].openinv(InventoryTile)
                            state["storage"] = []
                            for i in range(len(newinv["class"].tab)):
                                state["storage"].append([])
                                for j in range(len(newinv["class"].tab[i])):
                                    state["storage"][i].append({})
                                    if(newinv["class"].tab[i][j].acceptItem):
                                        state["storage"][i][j] = {"item":newinv["class"].tab[i][j].item,"count":newinv["class"].tab[i][j].count}
                                    else:
                                        state["storage"][i][j] = {"item":None,"count":0}
                            """for i in newinv["class"].tab:
                                for j in i:
                                    if(j.acceptItem):
                                        print(j.item," ",j.count)
                                        s"""
                            #state["storage"] = [{"item":i.item,"count":i.count} for i in newinv]
                        openinvs.append(newinv)
                    else:
                        state["storage"] = []
                        for i in range(len(openinvs[openatindex]["class"].tab)):
                            state["storage"].append([])
                            for j in range(len(openinvs[openatindex]["class"].tab[i])):
                                state["storage"][i].append({})
                                if(openinvs[openatindex]["class"].tab[i][j].acceptItem):
                                    state["storage"][i][j] = {"item":openinvs[openatindex]["class"].tab[i][j].item,"count":openinvs[openatindex]["class"].tab[i][j].count}
                                else:
                                    state["storage"][i][j] = {"item":None,"count":0}
                        #state["storage"] = openinvs[openatindex]
                        del openinvs[openatindex]
                    map.setStateObject("map",rx,ry,state)
            inv = pygame.Rect(options["fen"]["width"]-32*9,options["fen"]["height"]-32,9*32,32)
            if(inv.collidepoint(pygame.mouse.get_pos())):
                x,y = pygame.mouse.get_pos()
                ux = x-(options["fen"]["width"]-32*9)
                ux//=32
                selected_inv = ux
        if event.type == pygame.QUIT: # croix rouge
            playing = False # On met à False donc la boucle s'arrête et le jeu se ferme
            print(tot/n*1000) # On affiche le temps moyen pour une frame
        if event.type == pygame.KEYDOWN and chatOpen:
            if event.key == K_ESCAPE:
                chatOpen = False
            if event.key == K_BACKSPACE:
                chatString = chatString[:-1]
            elif event.key == K_RETURN:
                chatOpen = False
                # PARSE COMMAND
                cmd = chatString.split(" ")
                if(cmd[0] == "give"):
                    if(cmd[1] in Item.nameToNumber and int(cmd[2]) > 0):
                        inventory.add(cmd[1],int(cmd[2]))
                if(cmd[0] == "setfps"):
                    maxFPSInt = int(cmd[1])
                chatString = ""
            else:
                chatString += event.unicode
        if event.type == pygame.KEYDOWN and not chatOpen: # Touche pressée
            if(event.key == 1073741882): # F1
                debug = not debug
            if event.key == K_z:
                yspeed = -1  # Vers le haut
                facing = "north"
            if event.key == K_s:
                yspeed = 1 # vers le bas
                facing = "south"
            if event.key == K_q:
                xspeed = -1 # Vers la gauche
                facing = "west"
            if event.key == K_d:
                xspeed = 1 # vers la droite
                facing = "east"
            if event.key == K_k:
                noclip = not noclip # On change l'état du noclip vers l'inverse
            if event.key == K_e:
                invOpen = not invOpen # On ouvre l'inventaire principal en mettant en pause cette fonction
            if event.key == K_c:
                fight.main(fen)
            if event.key == K_t:
                chatOpen = True
            if event.key == K_g: # Sauvegarde de la carte
                pass
                """
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
                """
            if event.key == K_o: # Pour tourner une tile compatible (Attention provoque un crash si pas déclarée comme tournable)
                if(editorActivated):
                    x,y = pygame.mouse.get_pos()
                    rx = int((x-(options["fen"]["width"]/2)+player.x*32)//32)
                    ry = int((y-(options["fen"]["height"]/2)+player.y*32)//32) # On fait des calculs pour trouver quelle case est cliquée
                    state = map.getStateObject("map",rx,ry)
                    if("rotID" in state):
                        if(state["rotID"] < state["maxrotID"]):
                            state["rotID"] += 1
                        else:
                            state["rotID"] = 0
                        map.setStateObject("map",rx,ry,state)
                    """
                    rot = int(map.gm(int(rx),int(ry))%1*10)
                    print(rot+1)
                    if(rot == 3):
                        map.modify(int(rx),int(ry),map.gm(int(rx),int(ry)) - 0.3)
                    else:
                        map.modify(int(rx),int(ry),map.gm(int(rx),int(ry)) + 0.1)
                    """
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
            if(event.key == K_ESCAPE):
                tk = tkinter.Tk()
                tkinter.Label(tk,text="Zeldo Options").pack()
                fps = tkinter.LabelFrame(tk,text="FPS max")
                fpsmax = tkinter.StringVar()
                tkinter.Spinbox(fps,textvariable=fpsmax,values=(maxFPSInt,30,60,75,120)).pack()
                fps.pack()
                size = tkinter.LabelFrame(tk,text="Résolution")
                sizeString = tkinter.StringVar()
                w,h = options["fen"]["width"],options["fen"]["height"]
                tkinter.Spinbox(size,textvariable=sizeString,values=(f"{w}x{h}","1920x1080","1080x720")).pack()
                size.pack()
                tk.mainloop()
                del tk
                try:
                    maxFPSInt = int(fpsmax.get())
                except:
                    maxFPSInt = 60
                try:
                    w,h = sizeString.get().split("x")
                    print(w)
                    print(h)
                    options["fen"]["width"] = int(w)
                    options["fen"]["height"] = int(h)
                    fen = pygame.display.set_mode((options["fen"]["width"], options["fen"]["height"]),DOUBLEBUF | RESIZABLE)
                except:
                    print("uwu")
                    options["fen"]["width"] = 1080
                    options["fen"]["height"] = 720
                    fen = pygame.display.set_mode((options["fen"]["width"], options["fen"]["height"]),DOUBLEBUF | RESIZABLE)
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
        if event.type == pygame.VIDEORESIZE:
            options["fen"]["width"] = event.w
            options["fen"]["height"] = event.h
            fen = pygame.display.set_mode((options["fen"]["width"], options["fen"]["height"]),DOUBLEBUF | RESIZABLE)
    perfReportEnd("events")
    perfReport("collisions")
    deltaWalk = time.time() - lastWalk
    lastWalk = time.time()
    coef = deltaWalk/(1/75)
    if(noclip):
        player.x+=xspeed*speed*coef
        player.y+=yspeed*speed*coef
        #print(Tile.tiles[map[int((player.x*32+10)//32)][int(floor(player.y))]].doPass,Tile.tiles[surmap[int((player.x*32+10)//32)][int(floor(player.y))]].doPass)
    else:
        try:
            if(xspeed == 1 and (Tile.tiles[int(map.gs(int((player.x*32+10)//32),int(floor(player.y)))//1)].doPass or Tile.tiles[int(map.gs(int((player.x*32+10)//32),int(floor(player.y)))//1)].needToPass in Item.items[Item.nameToNumber[inventory.tab[0][7].item]].effects) and (Tile.tiles[int(map.gm(int((player.x*32+10)//32),int(floor(player.y)))//1)].doPass or Tile.tiles[int(map.gm(int((player.x*32+10)//32),int(floor(player.y)))//1)].needToPass in Item.items[Item.nameToNumber[inventory.tab[0][7].item]].effects)):
                player.x+=xspeed*speed*coef
            if(xspeed == -1 and (Tile.tiles[int(map.gs(int((player.x*32-10)//32),int(floor(player.y)))//1)].doPass or Tile.tiles[int(map.gs(int((player.x*32-10)//32),int(floor(player.y)))//1)].needToPass in Item.items[Item.nameToNumber[inventory.tab[0][7].item]].effects) and (Tile.tiles[int(map.gm(int((player.x*32-10)//32),int(floor(player.y)))//1)].doPass or Tile.tiles[int(map.gm(int((player.x*32-10)//32),int(floor(player.y)))//1)].needToPass in Item.items[Item.nameToNumber[inventory.tab[0][7].item]].effects)):
                player.x+=xspeed*speed*coef
            if(yspeed == 1 and (Tile.tiles[int(map.gs(int(floor(player.x)),int((player.y*32+10)//32))//1)].doPass or Tile.tiles[int(map.gs(int(floor(player.x)),int((player.y*32+10)//32))//1)].needToPass in Item.items[Item.nameToNumber[inventory.tab[0][7].item]].effects) and (Tile.tiles[int(map.gm(int(floor(player.x)),int((player.y*32+10)//32))//1)].doPass or Tile.tiles[int(map.gm(int(floor(player.x)),int((player.y*32+10)//32))//1)].needToPass in Item.items[Item.nameToNumber[inventory.tab[0][7].item]].effects)):
                player.y+=yspeed*speed*coef
            if(yspeed == -1 and (Tile.tiles[int(map.gs(int(floor(player.x)),int((player.y*32-10)//32))//1)].doPass or Tile.tiles[int(map.gs(int(floor(player.x)),int((player.y*32-10)//32))//1)].needToPass in Item.items[Item.nameToNumber[inventory.tab[0][7].item]].effects) and (Tile.tiles[int(map.gm(int(floor(player.x)),int((player.y*32-10)//32))//1)].doPass or Tile.tiles[int(map.gm(int(floor(player.x)),int((player.y*32-10)//32))//1)].needToPass in Item.items[Item.nameToNumber[inventory.tab[0][7].item]].effects)):
                player.y+=yspeed*speed*coef
        except:
            if(xspeed == 1 and Tile.tiles[int(map.gs(int((player.x*32+10)//32),int(floor(player.y)))//1)].doPass and Tile.tiles[int(map.gm(int((player.x*32+10)//32),int(floor(player.y)))//1)].doPass):
                player.x+=xspeed*speed*coef
            if(xspeed == -1 and Tile.tiles[int(map.gs(int((player.x*32-10)//32),int(floor(player.y)))//1)].doPass and Tile.tiles[int(map.gm(int((player.x*32-10)//32),int(floor(player.y)))//1)].doPass):
                player.x+=xspeed*speed*coef
            if(yspeed == 1 and Tile.tiles[int(map.gs(int(floor(player.x)),int((player.y*32+10)//32))//1)].doPass and Tile.tiles[int(map.gm(int(floor(player.x)),int((player.y*32+10)//32))//1)].doPass):
                player.y+=yspeed*speed*coef
            if(yspeed == -1 and Tile.tiles[int(map.gs(int(floor(player.x)),int((player.y*32-10)//32))//1)].doPass and Tile.tiles[int(map.gm(int(floor(player.x)),int((player.y*32-10)//32))//1)].doPass):
                player.y+=yspeed*speed*coef
    perfReportEnd("collisions")
    if(editorActivated and editor_click):
        x,y = pygame.mouse.get_pos()
        rx = (x-(options["fen"]["width"]/2)+player.x*32)//32
        ry = (y-(options["fen"]["height"]/2)+player.y*32)//32
        if(Tile.tiles[id[0]].type == "surmap"):
            map.surmodify(int(rx),int(ry),id[0])
            if(Tile.tiles[id[0]].multiTile):
                state = {}
                state["rotID"] = 0
                state["maxrotID"] = len(Tile.tiles[id[0]].textures)-1
                #print(state)
                map.setStateObject("surmap",rx,ry,state)
        else:
            map.modify(int(rx),int(ry),id[0])
            if(Tile.tiles[id[0]].multiTile):
                state = {}
                state["rotID"] = 0
                state["maxrotID"] = len(Tile.tiles[id[0]].textures)-1
                #print(state)
                map.setStateObject("map",int(rx),int(ry),state)
    perfReport("drawMap")
    col = int(options["fen"]["height"]*(1/zoom)//32+3)
    lin = int(options["fen"]["width"]*(1/zoom)//32+3)
    xmin = player.x*32-(options["fen"]["width"]/2)*(1/zoom)+32
    ymin = player.y*32-(options["fen"]["height"]/2)*(1/zoom)+32
    filter = pygame.surface.Surface((options["fen"]["width"], options["fen"]["height"]))
    lumiere = floor(day_tick/36000*150)
    filter.fill((lumiere,lumiere,lumiere))
    x = xmin
    y = ymin
    for i in range(col):
        yc = y%32
        for j in range(lin):
            xc = x%32
            if(False):
                fen.blit(Tile.tiles[Tile.nameToNumber["darkeau"]].texture,(j*32-xc,i*32-yc))
            else:
                yz = floor(y/32)
                xz = floor(x/32)
                if(map.gm(int(xz-1),int(yz-1))%1 == 0):
                    case = Tile.tiles[map.gm(int(xz-1),int(yz-1))]
                    if(case.lightness == 1):
                        pygame.draw.circle(filter,(0, 0, 0),((j)*32-xc+16,(i)*32-yc+16),64)
                        """filter.blit(light,((j)*32-xc-50,(i)*32-yc-50))
                            filter.blit(light,((j)*32-xc-50+32,(i)*32-yc-50))
                            filter.blit(light,((j)*32-xc-50+32,(i)*32-yc-50+32))
                            filter.blit(light,((j)*32-xc-50,(i)*32-yc-50+32))"""
                    if(case.multiTile):
                        #xy = int(yz+xz)
                        texture = case.textures[map.getStateObject("map",int(xz-1),int(yz-1))["rotID"]]
                        #texture = texture[0]
                    else:
                        texture = case.texture
                    #texture2 = pygame.transform.scale(texture,(32*zoom+1,32*zoom+1))
                    fen.blit(texture,((j)*32*zoom-xc*zoom,(i)*32*zoom-yc*zoom))
                else:
                    rot = int(map.gm(int(xz-1),int(yz-1))%1*10)
                    #print(rot)
                    case = Tile.tiles[int(map.gm(int(xz-1),int(yz-1))//1)]
                    if(case.lightness == 1):
                        pygame.draw.circle(filter,(0, 0, 0),((j)*32-xc+16,(i)*32-yc+16),64)
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
                        
                        case = Tile.tiles[map.gs(int(xz-1),int(yz-1))]
                        if(case.lightness == 1):
                            pygame.draw.circle(filter,(0, 0, 0),((j)*32-xc+16,(i)*32-yc+16),64)
                            """filter.blit(light,((j)*32-xc-50,(i)*32-yc-50))
                                filter.blit(light,((j)*32-xc-50+32,(i)*32-yc-50))
                                filter.blit(light,((j)*32-xc-50+32,(i)*32-yc-50+32))
                                filter.blit(light,((j)*32-xc-50,(i)*32-yc-50+32))"""
                        if(case.multiTile):
                            #xy = int(yz+xz)
                            texture = case.textures[map.getStateObject("map",int(xz-1),int(yz-1))["rotID"]]
                        else:
                            texture = Tile.tiles[map.gs(int(xz-1),int(yz-1))].texture
                    except AttributeError:
                        texture = Tile.tiles[0].texture
                    #texture2 = pygame.transform.scale(texture,(32*zoom+1,32*zoom+1))
                    fen.blit(texture,((j)*32*zoom-xc*zoom,(i)*32*zoom-yc*zoom))
            x+=32
        x = xmin
        y+=32
    perfReportEnd("drawMap")
    if(facing == "south"):
        fen.blit(player.texture,(options["fen"]["width"]/2-16,options["fen"]["height"]/2-16))
        try:
            if(Item.items[Item.nameToNumber[inventory.tab[0][7].item]].textureonperso != None):
                fen.blit(Item.items[Item.nameToNumber[inventory.tab[0][7].item]].textureonperso,(options["fen"]["width"]/2-16,options["fen"]["height"]/2-16))
        except:
            pass
    elif(facing == "north"):
        fen.blit(player.back,(options["fen"]["width"]/2-16,options["fen"]["height"]/2-16))
    elif(facing == "east"):
        fen.blit(player.droite,(options["fen"]["width"]/2-16,options["fen"]["height"]/2-16))
    else:
        fen.blit(player.gauche,(options["fen"]["width"]/2-16,options["fen"]["height"]/2-16))
    map.draw_others(fen,player,options)
    fen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGB_SUB)
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
        
    for i in openinvs:
        for k in range(5):
            for j in range(5):
                x = (i["x"]+0.5)*32 + k*32 - player.x*32 + options["fen"]["width"]/2
                y = (i["y"]+0.5)*32 + j*32 - player.y*32 + options["fen"]["height"]/2
                fen.blit(i["class"].tab[k][j].get_texture(),(x,y))
    if(drag):
        texture = Item.items[Item.nameToNumber[dragged_Item]].texture
        x,y = pygame.mouse.get_pos()
        x = x-drag_x
        y = y-drag_y
        fen.blit(texture,(x,y))
        x,y = pygame.mouse.get_pos()
        rx = int((x-(options["fen"]["width"]/2)+player.x*32)//32)
        ry = int((y-(options["fen"]["height"]/2)+player.y*32)//32)
        x = rx*32-player.x*32+options["fen"]["width"]/2
        y = ry*32-player.y*32+options["fen"]["height"]/2
        x0 = options["fen"]["width"] - 9*32 # On calcule la position en haut à gauche de l'inventaire
        y0 = options["fen"]["height"] - 9*32
        xm,ym = pygame.mouse.get_pos()
        xm-=x0 # On calcule la position sur le référentiel de l'inventaire (en partant du coin)
        ym-=y0
        pose = Item.items[Item.nameToNumber[dragged_Item]].blockpose
        if((pose != "") and (not(xm > 0 and ym > 0) or not invOpen)):

            s = Tile.tiles[Tile.nameToNumber[pose]].texture
            fen.blit(s,(x,y))
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
    #classes.mobs.draw_vache(fen,player,cmap,Tile,options)
    #classes.mobs.draw_vache(fen,player,cmap,Tile,options)
    #classes.mobs.draw_vache(fen,player,cmap,Tile,options)
    

    img = font.render('VERSION ALPHA - Zeldo + EDITOR - Projet NSI', True, (255,255,255))
    fen.blit(img, (20, 32))
    if(debug):
        img = font.render('PosX: {}'.format(player.x), True, (255,255,255))
        fen.blit(img, (20, 64))
        img = font.render('PosY: {}'.format(player.y), True, (255,255,255))
        fen.blit(img, (20, 96))
        FPS = str(int(clock.get_fps()))
        img = font.render('FPS: {}/{}'.format(FPS,maxFPSInt), True, (255,255,255))
        fen.blit(img, (20, 128))
        img = font.render('Server: {}'.format(map.getServer()), True, (255,255,255))
        fen.blit(img, (20, 160))
        img = font.render('Dragged Item: {}'.format(dragged_Item), True, (255,255,255))
        fen.blit(img, (20, 224))
        img = font.render('Dragged Item Number: {}'.format(dragged_Item_count), True, (255,255,255))
        fen.blit(img, (20, 256))
        img = font.render('No clip: {}'.format(noclip), True, (255,255,255))
        fen.blit(img, (20, 256+32))
        img = font.render('Zoom {}'.format(zoom), True, (255,255,255))
        fen.blit(img, (20, 256+64))
        img = font.render('Chunks loaded {}'.format(map.chunksLoaded()), True, (255,255,255))
        fen.blit(img, (20, 256+96))
    if(going < 0):
        hour = (36000-day_tick)//3000
        temp = (36000-day_tick)-(hour*3000)
        minute = floor(temp/3000*60)
    else:
        hour = day_tick//3000
        temp = day_tick-(hour*3000)
        minute = floor(temp/3000*60)
        hour+=12
    if(debug):
        img = font.render('Time: {}h{}'.format(hour,minute), True, (255,255,255))
        fen.blit(img, (20, 192))
    if(debug):
        pygame.draw.line(fen,(51,51,51),(50,options["fen"]["height"]-20-(1/75)*3000),(350,options["fen"]["height"]-20-(1/75)*3000))
        framesTimes = getReport("frame")[-100:]
        j = 0
        for i in framesTimes:
            f = 1/i
            if(f >= 70):
                c = (0,255,0)
            elif(f >= 59):
                c = (252, 186, 3)
            else:
                c = (255,0,0)
            pygame.draw.line(fen,c,(50+j*3,options["fen"]["height"]-20),(50+j*3,options["fen"]["height"]-20-i*3000),width=3)
            j+=1
    if(chatOpen):
        img = font.render(chatString, True, (255,255,255))
        w,h = img.get_size()
        sur = pygame.surface.Surface((w+10,h+10))
        sur.fill((51,51,51))
        sur.blit(img,(5,5))
        fen.blit(sur, (20, options["fen"]["height"]-48))
    pygame.display.flip()
    #os.system("pause")
    tot += (time.time() - lastTime)
    n+= 1
    perfReportEnd("frame")
    clock.tick(maxFPSInt)
map.saveAllChunks()
printReports()
pygame.quit()
logFile.close()
logFileError.close()