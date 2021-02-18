import socket
import pickle
import json
import time
from _thread import *
n = 0
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(("127.0.0.1", 8081))
ss.listen(5)
modifs = []
clients = []
poses = {}
conversion,map,surmap = json.loads(open("..\\map.json",'r').read()) # on charge la map depuis le fichier
def threaded_client(conn):
    global map,surmap
    while True:
        try:
            try:
                data = conn.recv(2048*32).decode("utf-8")
            except ConnectionResetError:
                print("Disconnected")
                clients.remove(conn)
                break
            if not data:
                print("Disconnected")
                clients.remove(conn)
                break
            else:
                #print(data)
                data = json.loads(data)
                if(data[0] == "mod"):
                    if(data[1] == "map"):
                        map[data[2]][data[3]] = data[4]
                        modifs.append((data,conn))
                    if(data[1] == "surmap"):
                        surmap[data[2]][data[3]] = data[4]
                        modifs.append((data,conn))
                elif(data[0] == "pos"):
                    poses[conn.getpeername()] = (data[1],data[2])
        except error as e:
            break
            print(e)
def server_thread():
    global modifs

    while True:
        time.sleep(0.02)
        print(clients)
        try:
            toSend = []
            uwu = modifs
            if(len(modifs) > 0):
                for i,j in enumerate(modifs):
                    o = modifs.pop(i)
                    t = json.dumps(o[0]).encode()
                    for u in clients:
                        u.send(t)
            modifs = []
            l = []
            for i,j in enumerate(poses):
                l.append(poses[j])
            s = json.dumps(("pos",l)).encode()
            h = []
            for i in l:
                h.append(i)
            o = json.dumps(("pos",l)).encode()
            for u in clients:
                u.send(o)
        except error as e:
            print(e)
start_new_thread(server_thread,())
while True:
    try:
        conn , addr = ss.accept()
        print("{} connected".format(addr))
        jzon = json.dumps((conversion,map,surmap))
        conn.send(jzon.encode())
        n+=1
        start_new_thread(threaded_client,(conn,))
        clients.append(conn)

    except error as e:
        print(e)
