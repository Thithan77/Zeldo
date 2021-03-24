import socket
import _thread
import sys
import json
import copy
from random import randint
server = "192.168.1.48"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
updates = {}
positions = {}
try:
    s.bind((server,port))
except socket.error as e:
    str(e)
if(sys.platform == "linux"):
    conversion,map,surmap = json.loads(open("../map.json",'r').read()) # on charge la map depuis le fichier
else:
    conversion,map,surmap = json.loads(open("..\\map.json",'r').read()) # on charge la map depuis le fichier
maps = {}
maps["main"] = {}
maps["main"]["map"] = map
maps["main"]["surmap"] = surmap
maps["main"]["updates"] = {}
maps["main"]["positions"] = {}
s.listen(2)
print("Server started ! Waiting for connexion ...")

def threaded_client(conn):
    map = "main"
    name = conn.getpeername()
    print("New client !")
    maps[map]["updates"][conn.getpeername()] = []
    maps[map]["positions"][conn.getpeername()] = (0,0,"uwu")
    while True:
        try:
            data = conn.recv(2048)
            jzon = json.loads(data.decode())
        except:
            print("AIE AIE AIE")
            print(f"client {name} disconnected")
            del maps[map]["updates"][name]
            del maps[map]["positions"][name]
            break
        #print(f"Data : {data}")
        for u in jzon:
            #print(f"u: {u}")
            for i,j in enumerate(updates):
                if(j != conn.getpeername()):
                    if(u[0] != "pos"):
                        maps[map]["updates"][j].append(u)
            if(u[0] == "modmap"):
                map[u[1]][u[2]] = u[3]
            elif(u[0] == "modsurmap"):
                surmap[u[1]][u[2]] = u[3]
            elif(u[0] == "pos"):
                maps[map]["positions"][conn.getpeername()] = (u[1],u[2],u[3])
            elif(u[0] == "changeMap"):
                if(u[1] == "newGame"):
                    print("Nouvelle map")
                    rand = randint(1,10000)
                    map = rand
                    if(rand not in maps):
                        maps[rand] = {}
                        maps[rand]["map"] = map
                        maps[rand]["surmap"] = surmap
                        maps[rand]["updates"] = {}
                        maps[rand]["positions"] = {}
                        conn.send(str.encode(json.dumps(("newMap",(conversion,map,surmap)))))
                        print("Uwu")
                        print(conn.recv(2048).decode())
                else:
                    map = u[1]
        reply = maps[map]["updates"][conn.getpeername()]
        for i,j in enumerate(positions):
            if(j!=conn.getpeername()):
                u = maps[map]["positions"][j]
                reply.append(("pos",u[0],u[1],u[2]))
        maps[map]["updates"][conn.getpeername()] = []
        if not data:
            print(f"client {conn.getpeername()} disconnected")
            del maps[map]["updates"][conn.getpeername()]
            del maps[map]["positions"][conn.getpeername()]
        else:
            """
            print(f"Received {data}")
            print(f"Sending {reply}")
            """
        conn.send(str.encode(json.dumps(reply)))
while True:
    conn,addr = s.accept()
    conn.send(str.encode(json.dumps((conversion,map,surmap))))
    print(f"{addr} just connected !")
    _thread.start_new_thread(threaded_client,(conn,))
