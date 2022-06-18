import classes.map as cmap
import socket
import _thread
import sys
import json
import copy
import tkinter
import classes.Tile
from random import randint
import pygame
pygame.init()
fen = pygame.display.set_mode((1,1),pygame.HIDDEN) # On définit la fenêtre à la taille indiquée
from init import *
server = "localhost"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
updates = {}
positions = {}
try:
    s.bind((server,port))
except socket.error as e:
    str(e)
s.listen(2)
print("Server started ! Waiting for connexion ...")

maps = {}
maps["lobby"] = {}
maps["lobby"]["map"] = cmap.NewMap(Tile,sys.argv,"lobby")
maps["lobby"]["updates"] = {}
maps["lobby"]["positions"] = {}
maps["lobby"]["waitingChunks"] = {}
def threaded_client(conn):
    map = "lobby"
    name = conn.getpeername()
    print(f"Nouveau client {name}")
    connected = True
    maps["lobby"]["updates"][name] = []
    maps["lobby"]["positions"][name] = (0,0,"PlaceHolder")
    maps["lobby"]["waitingChunks"][name] = []
    while connected:
        up = maps[map]["updates"][name]
        maps[map]["updates"][name] = []
        for i in maps["lobby"]["waitingChunks"][name]:
            if i in maps["lobby"]["map"].loadedChunks:
                maps[map]["updates"][name].append(("fullChunk",i,maps[map]["map"].Map[i]))
                maps["lobby"]["waitingChunks"][name].remove(i)
        for i in maps["lobby"]["positions"]:
            if(i != name):
                up.append(("pos",maps["lobby"]["positions"][i]))
        jzon = json.dumps(up)
        conn.send(str.encode(jzon))
        try:
            data = conn.recv(2048)
            #print(data.decode())
            jzon = json.loads(data.decode())
        except:
            print("AIE AIE AIE")
            print(f"client {name} disconnected")
            del maps[map]["updates"][name]
            del maps[map]["positions"][name]
            connected = False
            break
        for u in jzon:
            if(u[0] == "askChunk"):
                print((u[1][0],u[1][1]))
                if((u[1][0],u[1][1]) in maps[map]["map"].loadedChunks):
                    maps[map]["updates"][name].append(("fullChunk",(u[1][0],u[1][1]),maps[map]["map"].Map[u[1][0],u[1][1]]))
                else:
                    maps["lobby"]["updates"][name].append(("message",f"Loading chunk {u[1][0]}:{u[1][1]} please wait"))
                    maps["lobby"]["waitingChunks"][name].append((u[1][0],u[1][1]))
                    print(maps[map]["map"].gm(u[1][0]*16+1,u[1][1]*16+1))
            elif(u[0] == "mod"):
                print("modifying")
                maps[map]["map"].modify(u[1][0],u[1][1],u[2])
                for i in maps[map]["updates"]:
                    maps[map]["updates"][i].append(u)
            elif(u[0] == "surmod"):
                print("surmodifying")
                maps[map]["map"].surmodify(u[1][0],u[1][1],u[2])
                for i in maps[map]["updates"]:
                    maps[map]["updates"][i].append(u)
            elif(u[0] == "pos"):
                maps[map]["positions"][name] = (u[1],u[2],u[3])
            elif(u[0] == "ping"):
                maps[map]["updates"][name].append(u)
while True:
    print("Boucle")
    conn,addr = s.accept()
    print(f"Connexion de {addr}")
    _thread.start_new_thread(threaded_client,(conn,))