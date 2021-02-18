import socket
import pickle
import json
import time
from _thread import *
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(("127.0.0.1", 8081))
ss.listen(5)
modifs = []
clients = []
poses = []
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
                print(data)
                data = json.loads(data)
                if(data[0] == "mod"):
                    if(data[1] == "map"):
                        print("yolo")
                        map[data[2]][data[3]] = data[4]
                    if(data[1] == "surmap"):
                        surmap[data[2]][data[3]] = data[4]

                modifs.append((data,conn))
        except error as e:
            break
            print(e)
def server_thread():
    global modifs

    while True:
        time.sleep(0.02)
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
            """
            s = json.dumps(("pos",poses)).encode()
            for u in clients:
                u.send(s)
            """
        except error as e:
            print(e)
start_new_thread(server_thread,())
while True:
    try:
        conn , addr = ss.accept()
        print("{} connected".format(addr))
        jzon = json.dumps((conversion,map,surmap))
        conn.send(jzon.encode())
        start_new_thread(threaded_client,(conn,))
        clients.append(conn)

    except error as e:
        print(e)
