import json
import socket
from _thread import *
import time
from perlin_noise import PerlinNoise
noise = PerlinNoise(octaves=0.1, seed=648325)
def threaded_map():
    while True:
        try:
            data = multiMap.socket.recv(2048*16).decode("utf-8")
            data = data.split("]]")[0] + "]]"
            print(data)
            if not data:
                print("Disconnected")
                break
            else:
                data = json.loads(data)
                if(data[0] == "mod"):
                    if(data[1] == "map"):
                        multiMap.map[data[2]][data[3]] = data[4]
                    if(data[1] == "surmap"):
                        multiMap.surmap[data[2]][data[3]] = data[4]
                elif(data[0] == "pos"):
                    del multiMap.poses
                    multiMap.poses = data[1]
                    print(data[1])
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
    socket
    map = []
    surmap = []
    poses = []
    def __init__(self,Tile,argv):
        multiMap.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        multiMap.socket.connect(("127.0.0.1",8081))
        data = multiMap.socket.recv(2048*128).decode("utf-8")
        conv,multiMap.map,multiMap.surmap = json.loads(data)
        start_new_thread(threaded_map,())
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
        mod = ("mod","map",i,j,val)
        p = json.dumps(mod).encode()
        multiMap.socket.send(p)
    def surmodify(self,i,j,val):
        multiMap.surmap[i][j] = val
    def draw_others(self,fen,player,options):
        multiMap.socket.send(json.dumps(("pos",player.x,player.y)).encode())
        for i,j in enumerate(multiMap.poses):
            x = (j[0]*32-player.x*32+options["fen"]["width"]/2)-16
            y = (j[1]*32-player.y*32+options["fen"]["height"]/2)-16
            print((x,y))
            fen.blit(player.texture,(x,y))
