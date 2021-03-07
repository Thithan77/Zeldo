import socket
import _thread
import sys
import json
import copy
server = "192.168.1.48"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
updates = {}
positions = {}
try:
    s.bind((server,port))
except socket.error as e:
    str(e)
conversion,map,surmap = json.loads(open("..\\map.json",'r').read()) # on charge la map depuis le fichier
s.listen(2)
print("Server started ! Waiting for connexion ...")

def threaded_client(conn):
    print("New client !")
    updates[conn.getpeername()] = []
    positions[conn.getpeername()] = (0,0)
    while True:
        data = conn.recv(2048).decode()
        jzon = json.loads(data)
        #print(f"Data : {data}")
        for u in jzon:
            #print(f"u: {u}")
            for i,j in enumerate(updates):
                if(j != conn.getpeername()):
                    if(u[0] != "pos"):
                        updates[j].append(u)
            if(u[0] == "modmap"):
                map[u[1]][u[2]] = u[3]
            elif(u[0] == "modsurmap"):
                surmap[u[1]][u[2]] = u[3]
            elif(u[0] == "pos"):
                positions[conn.getpeername()] = (u[1],u[2])
        reply = updates[conn.getpeername()]
        for i,j in enumerate(positions):
            if(j!=conn.getpeername()):
                u = positions[j]
                reply.append(("pos",u[0],u[1]))
        updates[conn.getpeername()] = []
        if not data:
            print(f"client {conn.getpeername()} disconnected")
            del updates[conn.getpeername()]
            del positions[conn.getpeername()]
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
