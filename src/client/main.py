import socket
import json
import datetime
import threading

IPADDR = "3.144.35.135"
PORT = 49153
NAME = str(input("\nuser name\n>>>"))
CHANNEL = "global"
BUFFER_SIZE = 1024

CHARSET = "UTF-8"

def recver(sock):
    while True:
        try:
            data = sock.recv(BUFFER_SIZE)
            recv = json.loads(data.decode(CHARSET))
            #recv = pickle.loads(data)
            if recv["channel"] == CHANNEL:
                print(f'\n[{recv["name"]}]:{recv["date"]}\n{recv["content"]}')
            else:
                pass
        except ConnectionResetError:
            break
        except json.decoder.JSONDecodeError:
            pass
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

sock = socket.socket(socket.AF_INET)
sock.connect((IPADDR, PORT))
#send_data = pickle.dumps({"name":NAME,"channel":CHANNEL,"type":"user","content":""})
send_data = json.dumps({"name":NAME,"channel":CHANNEL,"type":"user","content":""}).encode(CHARSET)
sock.send(send_data)
print('you type "/exit" to exit')
thread = threading.Thread(target=recver, args=(sock,))
thread.start()
while True:
    content = input()
    print("\033[1A\033[2K")
    if content == "":
        continue
    if content == "/exit":
        break
    elif content == "/ch":
        print(f"channel={CHANNEL}")
    elif content == "/goto":
        CHANNEL = "global"
        print(f"moved to {CHANNEL}")
    elif content.startswith("/goto "):
        CHANNEL = content.replace("/goto ","")
        print(f"moved to {CHANNEL}")
    else:
        try:
            date = datetime.datetime.now()
            now = f'{date.month}/{date.day} {date.hour}:{date.minute}'
            #send_data = pickle.dumps({"name":NAME,"channel":CHANNEL,"date":now,"type":"user","content":content})
            send_data = json.dumps({"name":NAME,"channel":CHANNEL,"date":now,"type":"user","content":content}).encode(CHARSET)
            sock.send(send_data)
        except ConnectionResetError:
            break

sock.shutdown(socket.SHUT_RDWR)
sock.close()