import json
import socket
from _thread import *
import time
import copy
from perlin_noise import PerlinNoise
noise = PerlinNoise(octaves=0.1, seed=648325)
others = []
def threaded_map(player):
    global others
    while True:
        try:
            updates = multiMap.updates
            updates.append(("pos",player.x,player.y))
            multiMap.updates = []
            jzon = json.dumps(updates)
            multiMap.socket.send(jzon.encode())
            data = multiMap.socket.recv(2048*16).decode("utf-8")
            data = json.loads(data)
            newothers = []
            for i in data:
                if(i[0] == "modmap"):
                    multiMap.map[i[1]][i[2]] = i[3]
                elif(i[0] == "modsurmap"):
                    multiMap.surmap[i[1]][i[2]] = i[3]
                elif(i[0] == "pos"):
                    newothers.append((i[1],i[2]))
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
    def __init__(self,a,b,player):
        self.server = "89.89.197.173"
        self.port = 8081
        self.addr = (self.server,self.port)
        multiMap.socket.connect(self.addr)
        recv = multiMap.socket.recv(2048*250).decode("utf-8")
        multiMap.conv,multiMap.map,multiMap.surmap = json.loads(recv)
        start_new_thread(threaded_map,(player,))
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
