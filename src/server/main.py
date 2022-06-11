import socket
import pickle
import threading
import datetime
import json
from logger import logger

IPADDR = "0.0.0.0"
PORT = 49153
BUFFER_SIZE = 1024
CHARSET = "UTF-8"
clients = []
users = {}
logg = logger("server","info")

def recver(conn, addr):
    while True:
        try:
            recv = conn.recv(BUFFER_SIZE)
            data = json.loads(recv.decode(CHARSET,"ignore"))
            users[addr] = [data["name"],data["channel"]]
            for client in clients:
                client[0].send(recv)
        except:
            break
    clients.remove((conn, addr))
    logg.info(f" {users[addr][0]} learved addr={addr} channel={users[addr][1]}")
    date = datetime.datetime.now()
    now = f'{date.month}/{date.day} {date.hour}:{date.minute}'
    for client in clients:
        try:
            #client[0].send(pickle.dumps({"name":"Server","channel":users[addr][1],"date":now,"type":"bot","content":f"{users[addr][0]} learved"}))
            client[0].send(json.dumps({"name":"Server","channel":users[addr][1],"date":now,"type":"bot","content":f"{users[addr][0]} learved"}).encode(CHARSET))
        except BrokenPipeError:
            clients.remove(client)
            continue
    try:
        conn.shutdown(socket.SHUT_RDWR)
    except:
        logg.warning(" Transport endpoint is not connected")
    conn.close()

sock = socket.socket(socket.AF_INET)
sock.bind((IPADDR, PORT))
sock.listen()

logg.info(" Welcome to Simple-chat")
logg.warning(f" ip={IPADDR},port={PORT},buffersize={BUFFER_SIZE}")

while True:
    conn, addr = sock.accept()
    try:
        data = conn.recv(BUFFER_SIZE)
        #data = pickle.loads(data)
        data = json.loads(data.decode(CHARSET,"ignore"))
    except ConnectionResetError:
        logg.error(f" Connection has been reset {addr}")
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        continue
    except json.decoder.JSONDecodeError:
        continue
    clients.append((conn, addr))
    users[addr] = [data["name"],data["channel"]]
    logg.info(f" {users[addr][0]} joined addr={addr} channel={users[addr][1]}")
    date = datetime.datetime.now()
    now = f'{date.month}/{date.day} {date.hour}:{date.minute}'
    for client in clients:
        try:
            #client[0].send(pickle.dumps({"name":"Server","channel":users[addr][1],"date":now,"type":"bot","content":f"{users[addr][0]} joined"}))
            client[0].send(json.dumps({"name":"Server","channel":users[addr][1],"date":now,"type":"bot","content":f"{users[addr][0]} joined"}).encode(CHARSET))
        except BrokenPipeError:
            clients.remove(client)
            continue
    thread = threading.Thread(target=recver, args=(conn, addr))
    thread.start()