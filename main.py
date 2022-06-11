import socket, json, logging, datetime, threading

config_path = __file__.replace("main.py","")+"config.json"
try:
    config = json.load(open(config_path))
except FileNotFoundError:
    config = {
        "IPADDR": "0.0.0.0",
        "PORT": 49153,
        "BUFFER_SIZE": 1024,
        "CHARSET": "UTF-8",
        "IPV": 0,
    }
    f = open(config_path,"wt")
    f.write(json.dumps(config))
IPADDR = config["IPADDR"]
PORT = config["PORT"]
BUFFER_SIZE = config["BUFFER_SIZE"]
CHARSET = config["CHARSET"]
IPV = [socket.AF_INET,socket.AF_INET6][config["IPV"]]

sock = socket.socket(socket.AF_INET)
sock.bind((IPADDR, PORT))
sock.listen()
clients = {}

def receiver(conn):
    while True:
        try:
            data = conn.recv(config["BUFFER_SIZE"])
            data = json.loads(data.decode(CHARSET,"ignore"))
        except (ConnectionResetError, json.decoder.JSONDecodeError):
            conn.close()
            break
        for client in clients.keys():
            if data["channel"] == clients[client][1]:
                try:
                    clients[client][0].send(json.dumps({"name":data["name"],"channel":data["channel"],"date":data["date"],"type":data["type"],"content":f"{data['content']}"}).encode(CHARSET))
                except BrokenPipeError:
                    clients.pop(client)
                    continue
    conn.close()

while True:
    #接続待ち
    conn, addr = sock.accept()
    try:
        data = conn.recv(config["BUFFER_SIZE"])
        data = json.loads(data.decode(CHARSET,"ignore"))
    except (ConnectionResetError, json.decoder.JSONDecodeError):
        conn.close()
        continue
    clients[data["UUID"]] = (conn,data["channel"])
    #参加メッセージ
    for client in clients.keys():
        if data["channel"] == clients[client][1]:
            try:
                clients[client][0].send(json.dumps({"name":"Server","channel":data["channel"],"date":data["date"],"type":"bot","content":f"{data['name']} joined"}).encode(CHARSET))
            except BrokenPipeError:
                clients.pop(client)
                continue
    thread = threading.Thread(target=receiver, args=(conn,))
    thread.start()
