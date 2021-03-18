import socket
import _thread
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server = "127.0.0.1"
port = 8081
addr = (server,port)
def connect():
    try:
        client.connect(addr)
        data = client.recv(2048)
        print(data.decode("utf-8"))
    except:
        print("Disconnected !")
connect()
def send(data):
    try:
        client.send(str.encode(data))
        return client.recv(2048).decode()
    except socket.error as e:
        print(e)
print(send("Hey"))
