import socket
from _thread import *
import pickle
from game import Game
from operator import add

server = "192.168.1.135" # "127.0.0.1"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
    print("socket successfully created")
except socket.error as e:
    print(f"socket creation failed with error {err}")

s.listen() # s.listen(2) # idk which, shouldn't matter?
print("server started")

p = 0 # i.e. player 0, player 1, player 2, ... currently only supports player0 and player 1

def threaded_client(conn, _p, game):
    conn.send(str.encode(str(_p)))
    while True:
        try:
            data = pickle.loads(conn.recv(2048*2)) # tuple corresponding a movmenet unless otherwise
            if data == "get": # NOT SURE HOW TO WORK IT
                pass
            elif data:
                print(f"data is {data}")
                game.ppos[_p] = list(map(add, game.ppos[_p], data))
            else:
                pass
            conn.sendall(pickle.dumps(game))
        except error as e:
            print(e)
            break
    print("Lost connection")
    global p
    p -= 1
    conn.close()

game = Game()
print("Creating a new game...")
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, p, game))
    print(p)
    p += 1 # for next time