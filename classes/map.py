import json
import socket
from _thread import *
import time
import copy
import pygame
import os
from perlin_noise import PerlinNoise
noise = PerlinNoise(octaves=0.1, seed=648325)
others = []
def threaded_map(player,pseudo):
    global others
    while True:
        try:
            updates = multiMap.updates
            updates.append(("pos",player.x,player.y,pseudo))
            multiMap.updates = []
            jzon = json.dumps(updates)
            multiMap.socket.send(jzon.encode())
            rcv = True
            data = multiMap.socket.recv(2048*16).decode("utf-8")
            print(data)
            if("][" in data):
                data = data.split("][")[0] + "]"
            while rcv:
                try:
                    if(data != "" or data != "[][]"):
                        dataJ = json.loads(data)
                except json.JSONDecodeError as e:
                    print(e)
                    print("Et on repart pour un tour !")
                    data+= multiMap.socket.recv(2048*16).decode()
                    print(data)
                else:
                    rcv = False
            newothers = []
            for i in dataJ:
                if(i[0] == "modmap"):
                    multiMap.map[i[1]][i[2]] = i[3]
                elif(i[0] == "modsurmap"):
                    multiMap.surmap[i[1]][i[2]] = i[3]
                elif(i[0] == "pos"):
                    newothers.append((i[1],i[2],i[3]))
                elif(i[0] == "newMap"):
                    multiMap.conv,multiMap.map,multiMap.surmap = i[1]
                    print(f"Hey :{multiMap.surmap}")
                    print("Chargement de la map terminé !")
                    multiMap.socket.send("oki".encode("utf-8"))
                    print("Oki envoyé")
                elif(i[0] == "mapName"):
                    multiMap.serverName = i[1]
            others = copy.copy(newothers)
        except error as e:
            print(e)
class Map:
    def __init__(self,Tile,argv):
        self.map = []
        self.surmap = []
        conversion,self.map,self.surmap = json.loads(open("map.json",'r').read()) # on charge la map depuis le fichier
        toConvert = {}
        needConvert = False
        for i in conversion:
            if(Tile.tiles[Tile.nameToNumber[i["name"]]].id != i["id"]):
                print("Convertion nécessaire de la map")
                toConvert[i["id"]] = Tile.tiles[Tile.nameToNumber[i["name"]]].id
                needConvert = True
            else:
                toConvert[i["id"]] = Tile.tiles[Tile.nameToNumber[i["name"]]].id
        if(needConvert):
            for i,j in enumerate(self.map):
                for k,l in enumerate(self.map[i]):
                    self.map[i][k] = toConvert[self.map[i][k]//1]+self.map[i][k]%1
            for i,j in enumerate(self.surmap):
                for k,l in enumerate(self.surmap[i]):
                    self.surmap[i][k] = toConvert[self.surmap[i][k]]
        if("perlin" in argv):
            for i in range(200):
                for j in range(200):
                    self.surmap[i][j] = Tile.nameToNumber["nada"]
                    k = noise([i,j])
                    if(k < -0.25):
                        self.map[i][j] = Tile.nameToNumber["eau"]
                    elif(k < -0.1):
                        self.map[i][j] = Tile.nameToNumber["sable"]
                    else:
                        self.map[i][j] = Tile.nameToNumber["gazon"]
                    if(k > 0.25):
                        self.surmap[i][j] = Tile.nameToNumber["arbre"]
    def getServer(self):
        return "local"
    def gm(self,i,j):
        xchunk = i//32
        ychunk = j//32
        return(self.map[i][j])
    def gs(self,i,j):
        xchunk = i//32
        ychunk = j//32
        return(self.surmap[i][j])
    def modify(self,i,j,val):
        self.map[i][j] = val
    def surmodify(self,i,j,val):
        self.surmap[i][j] = val
    def draw_others(self,fen,player,options):
        pass
class multiMap:
    map,surmap,conv = [],[],[]
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    updates = []
    serverName = "main"
    def __init__(self,a,b,player,pseudo):
        self.server = "192.168.1.82"
        self.port = 8081
        self.addr = (self.server,self.port)
        self.pseudo = pseudo
        multiMap.socket.connect(self.addr)
        self.font = pygame.font.SysFont(None, 14)
        recv = multiMap.socket.recv(2048*250).decode("utf-8")
        map_loaded = False
        while not map_loaded:
            try:
                multiMap.conv,multiMap.map,multiMap.surmap = json.loads(recv)
                map_loaded = True
                print("test")
            except json.JSONDecodeError:
                recv+= multiMap.socket.recv(2048*250).decode("utf-8")
        start_new_thread(threaded_map,(player,pseudo.get()))

    def gm(self,i,j):
        xchunk = i//32
        ychunk = j//32
        return(multiMap.map[i][j])
    def gs(self,i,j):
        xchunk = i//32
        ychunk = j//32
        return(multiMap.surmap[i][j])
    def modify(self,i,j,val):
        multiMap.map[i][j] = val
        self.updates.append(("modmap",i,j,val))
    def surmodify(self,i,j,val):
        multiMap.surmap[i][j] = val
        self.updates.append(("modsurmap",i,j,val))
    def draw_others(self,fen,player,options):
        global others
        for i in others:
            x = i[0]*32
            y = i[1]*32
            rx = x - player.x*32 + options["fen"]["width"]/2-16
            ry = y - player.y*32 + options["fen"]["height"]/2-16
            fen.blit(player.texture,(rx,ry))
            img = self.font.render(i[2], True, (255,255,255))
            fen.blit(img, (rx, ry-8))
    def getServer(self):
        return multiMap.serverName
chunkSize = 32
class NewMap:
    Map = {}
    loadedChunks = []
    loadingChunks = []
    nomMap = ""
    def __init__(self,Tile,argv,nomMap):
        self.map = []
        self.surmap = []
        self.Tile = Tile
        maps = os.listdir("maps/")
        if(nomMap not in maps):
            os.mkdir(f"maps/{nomMap}")
            os.mkdir(f"maps/{nomMap}/chunks")
        NewMap.nomMap = nomMap
        
    def getServer(self):
        return f"local+{NewMap.nomMap}"
    def gm(self,i,j):
        chunkX = i//chunkSize
        chunkY = j//chunkSize
        if((chunkX,chunkY) not in NewMap.loadedChunks):
            if((chunkX,chunkY) not in NewMap.loadingChunks):
                start_new_thread(loadChunk,(chunkX,chunkY))
                NewMap.loadingChunks.append((chunkX,chunkY))
            return 21
        else:
            c = NewMap.Map[(chunkX,chunkY)]["tiles"]["map"][i%chunkSize][j%chunkSize]
            return self.Tile.nameToNumber[c]
    def gs(self,i,j):
        chunkX = i//chunkSize
        chunkY = j//chunkSize
        if((chunkX,chunkY) not in NewMap.loadedChunks):
            if((chunkX,chunkY) not in NewMap.loadingChunks):
                start_new_thread(loadChunk,(chunkX,chunkY))
                NewMap.loadingChunks.append((chunkX,chunkY))
            return 12
        else:
            c = NewMap.Map[(chunkX,chunkY)]["tiles"]["surmap"][i%chunkSize][j%chunkSize]
            return self.Tile.nameToNumber[c]
    def modify(self,i,j,val):
        NewMap.Map[(i//chunkSize,j//chunkSize)]["tiles"]["map"][i%chunkSize][j%chunkSize] = self.Tile.tiles[val].name
    def surmodify(self,i,j,val):
        NewMap.Map[(i//chunkSize,j//chunkSize)]["tiles"]["surmap"][i%chunkSize][j%chunkSize] = self.Tile.tiles[val].name
    def draw_others(self,fen,player,options):
        pass
def loadChunk(x,y):
    chunks = os.listdir(f"maps/{NewMap.nomMap}/chunks")
    if(f"{x};{y}.json" in chunks):
        f = open(f"maps/{NewMap.nomMap}/chunks/{x};{y}.json",'r')
        txt = f.read()
        unjsoned = json.loads(txt)
        NewMap.Map[(x,y)] = unjsoned
        NewMap.loadedChunks.append((x,y))
        NewMap.loadingChunks.remove((x,y))
        f.close()
    else:
        f = open(f"maps/{NewMap.nomMap}/chunks/{x};{y}.json",'a')
        owo = {}
        lines = []
        noise = PerlinNoise(octaves=0.1, seed=abs(int(hash(NewMap.nomMap))))
        for i in range(chunkSize):
            lines.append("")
        owo["tiles"] = {}
        owo["tiles"]["map"] = []
        for i in range(chunkSize):
            owo["tiles"]["map"].append(copy.copy(lines))
        for i in range(chunkSize):
            for j in range(chunkSize):
                k = noise([(x*32+i)/2048,(y*32+j)/2048])
                if(k <= 0.0):
                    owo["tiles"]["map"][i][j] = "gazon"
                else:
                    owo["tiles"]["map"][i][j] = "eau"
        lines = []
        owo["tiles"]["surmap"] = []
        for i in range(chunkSize):
            lines.append("nada")
        for i in range(chunkSize):
            owo["tiles"]["surmap"].append(copy.copy(lines))
        jsoned = json.dumps(owo)
        NewMap.Map[(x,y)] = owo
        NewMap.loadedChunks.append((x,y))
        NewMap.loadingChunks.remove((x,y))
        f.write(jsoned)
        f.close()