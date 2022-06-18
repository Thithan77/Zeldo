import json
import socket
from _thread import *
import time
import copy
import pygame
import os
import pickle
from perlin_noise import PerlinNoise
noise = PerlinNoise(octaves=0.1, seed=648325)
others = []
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
