import json
import socket
from _thread import *
import time
import copy
from math import *
import pygame
import os
import pickle
from classes.bordel import *
from perlin_noise import PerlinNoise
print("Loading map file")
noise = PerlinNoise(octaves=0.1, seed=648325)
others = []
def threaded_map(player,pseudo):
    global others
    while True:
        try:
            updates = NewMultiMap.updates
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
def new_threaded_map(player,pseudo):
    print("Thread lanché")
    while True:
        updates = NewMultiMap.updates
        updates.append(("pos",player.x,player.y,pseudo))
        NewMultiMap.updates = []
        data = NewMultiMap.s.recv(2048*64)
        jzon = json.loads(data.decode())
        for u in jzon:
            if(u[0] == "message"):
                print(u[1])
            elif(u[0] == "fullChunk"):
                print(f"receveid chunk {(u[1][0],u[1][1])}")
                NewMultiMap.Map[(u[1][0],u[1][1])] = u[2]
                NewMultiMap.loadedChunks.append((u[1][0],u[1][1]))
                NewMultiMap.loadingChunks.remove((u[1][0],u[1][1]))
            elif(u[0] == "mod"):
                if((u[1][0]//16,u[1][1]//16) in NewMultiMap.loadedChunks):
                    NewMultiMap.Map[(u[1][0]//16,u[1][1]//16)]["tiles"]["map"][u[1][0]%chunkSize][u[1][1]%chunkSize] = NewMultiMap.Tile.tiles[u[2]].name
            elif(u[0] == "surmod"):
                if((u[1][0]//16,u[1][1]//16) in NewMultiMap.loadedChunks):
                    NewMultiMap.Map[(u[1][0]//16,u[1][1]//16)]["tiles"]["surmap"][u[1][0]%chunkSize][u[1][1]%chunkSize] = NewMultiMap.Tile.tiles[u[2]].name
            elif(u[0] == "pos"):
                NewMultiMap.others[u[1][2]] = (u[1][0],u[1][1])
            elif(u[0] == "ping"):
                NewMultiMap.lastPings.append((time.time() - u[1])*1000)
        jzon = json.dumps(updates)
        NewMultiMap.s.send(jzon.encode())
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
chunkSize = 16
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
        chunkX = i//chunkSize
        chunkY = j//chunkSize
        if((chunkX,chunkY) not in NewMap.loadedChunks):
            if((chunkX,chunkY) not in NewMap.loadingChunks):
                start_new_thread(loadChunk,(chunkX,chunkY))
                NewMap.loadingChunks.append((chunkX,chunkY))
            return
        else:
            NewMap.Map[(i//chunkSize,j//chunkSize)]["tiles"]["map"][i%chunkSize][j%chunkSize] = self.Tile.tiles[val].name
    def surmodify(self,i,j,val):
        chunkX = i//chunkSize
        chunkY = j//chunkSize
        if((chunkX,chunkY) not in NewMap.loadedChunks):
            if((chunkX,chunkY) not in NewMap.loadingChunks):
                start_new_thread(loadChunk,(chunkX,chunkY))
                NewMap.loadingChunks.append((chunkX,chunkY))
            return
        else:
            NewMap.Map[(i//chunkSize,j//chunkSize)]["tiles"]["surmap"][i%chunkSize][j%chunkSize] = self.Tile.tiles[val].name
    def draw_others(self,fen,player,options):
        pass
    def getStateObject(self,map,x,y):
        return NewMap.Map[(x//chunkSize,y//chunkSize)]["states"][map][x%chunkSize][y%chunkSize]
    def setStateObject(self,map,x,y,obj):
        NewMap.Map[(x//chunkSize,y//chunkSize)]["states"][map][x%chunkSize][y%chunkSize] = obj
    def chunksLoaded(self):
        return len(NewMap.Map)
    def saveChunk(self,xy):
        f = open(f"maps/{NewMap.nomMap}/chunks/{xy[0]};{xy[1]}.chunk",'wb')
        #jsoned = json.dumps(NewMap.Map[xy])
        #f.write(jsoned)
        pickle.dump(NewMap.Map[xy],f)
        f.close()
    def saveAllChunks(self):
        for c in NewMap.Map:
            self.saveChunk(c)
def loadChunk(x,y):
    print(f"Loading chunk {x}:{y}")
    chunks = os.listdir(f"maps/{NewMap.nomMap}/chunks")
    if(f"{x};{y}.chunk" in chunks):
        perfReport("loadChunk")
        f = open(f"maps/{NewMap.nomMap}/chunks/{x};{y}.chunk",'rb')
        #txt = f.read()
        #unjsoned = json.loads(txt)
        unjsoned = pickle.load(f)
        NewMap.Map[(x,y)] = unjsoned
        NewMap.loadedChunks.append((x,y))
        NewMap.loadingChunks.remove((x,y))
        f.close()
        perfReportEnd("loadChunk")
    else:
        perfReport("generateChunk")
        print("?")
        f = open(f"maps/{NewMap.nomMap}/chunks/{x};{y}.chunk",'wb')
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
        owo["states"] = {}
        owo["states"]["map"] = []
        owo["states"]["surmap"] = []
        lines = []
        for i in range(chunkSize):
            lines.append({})
        for i in range(chunkSize):
            owo["states"]["map"].append(copy.copy(lines))
            owo["states"]["surmap"].append(copy.copy(lines))
        #jsoned = json.dumps(owo)
        NewMap.Map[(x,y)] = owo
        NewMap.loadedChunks.append((x,y))
        NewMap.loadingChunks.remove((x,y))
        pickle.dump(owo,f)
        #f.write(jsoned)
        f.close()
        perfReportEnd("generateChunk")
    print(f"Loaded chunk {x}:{y}")
class NewMultiMap:
    Map = {}
    loadedChunks = []
    loadingChunks = []
    nomMap = "lobby"
    updates = []
    Tile = None
    others = {}
    s = None
    lastPings = []
    def __init__(self,Tile,argv,serverip,player,pseudo):
        self.map = []
        self.surmap = []
        self.Tile = Tile
        NewMultiMap.Tile = Tile
        self.ip,self.port = serverip.split(":")
        self.port = int(self.port)
        self.font = pygame.font.SysFont(None, 14)
        NewMultiMap.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        NewMultiMap.s.connect((self.ip, self.port))
        start_new_thread(new_threaded_map,(player,pseudo.get()))
    def getServer(self):
        NewMultiMap.updates.append(("ping",time.time()))
        s = 0
        for i in NewMultiMap.lastPings[-100:]:
            s += i
        ping = s/100
        return f"{self.ip}:{self.port}/{NewMultiMap.nomMap} + {floor(ping)}"
    def gm(self,i,j):
        chunkX = i//chunkSize
        chunkY = j//chunkSize
        if((chunkX,chunkY) not in NewMultiMap.loadedChunks):
            if((chunkX,chunkY) not in NewMultiMap.loadingChunks):
                NewMultiMap.updates.append(("askChunk",(chunkX,chunkY)))
                NewMultiMap.loadingChunks.append((chunkX,chunkY))
            return 21
        else:
            c = NewMultiMap.Map[(chunkX,chunkY)]["tiles"]["map"][i%chunkSize][j%chunkSize]
            return self.Tile.nameToNumber[c]
    def gs(self,i,j):
        chunkX = i//chunkSize
        chunkY = j//chunkSize
        if((chunkX,chunkY) not in NewMultiMap.loadedChunks):
            if((chunkX,chunkY) not in NewMultiMap.loadingChunks):
                NewMultiMap.updates.append(("askChunk",(chunkX,chunkY)))
                NewMultiMap.loadingChunks.append((chunkX,chunkY))
            return 12
        else:
            c = NewMultiMap.Map[(chunkX,chunkY)]["tiles"]["surmap"][i%chunkSize][j%chunkSize]
            return self.Tile.nameToNumber[c]
    def modify(self,i,j,val):
        NewMultiMap.updates.append(("mod",(i,j),val))
    def surmodify(self,i,j,val):
        NewMultiMap.updates.append(("surmod",(i,j),val))
    def draw_others(self,fen,player,options):
        for i in NewMultiMap.others:
            dx = NewMultiMap.others[i][0]*32 - player.x*32 + options["fen"]["width"]/2
            dy = NewMultiMap.others[i][1]*32 - player.y*32 + options["fen"]["height"]/2
            fen.blit(player.texture,(dx-16,dy-16))
            img = self.font.render(i, True, (255,255,255))
            fen.blit(img, (dx-16, dy-16-8))
    def getStateObject(self,map,x,y):
        return NewMultiMap.Map[(x//chunkSize,y//chunkSize)]["states"][map][x%chunkSize][y%chunkSize]
    def setStateObject(self,map,x,y,obj):
        pass
    def chunksLoaded(self):
        return len(NewMultiMap.Map)
    def saveChunk(self,xy):
        pass
    def saveAllChunks(self):
        pass
    def getPing():
        NewMultiMap.updates.append(("ping",time.time()))