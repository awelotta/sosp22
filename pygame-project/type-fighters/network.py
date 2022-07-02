import socket
import pickle

class Network:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #... need to change to match my code... I think this works though
        self.server = "192.168.1.135" # "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect() # indicates which player you are???
    def connect(self):
        try:
            self.s.connect(self.addr)
            return self.s.recv(2048).decode()
        except:
            pass
    def send(self, data):
        try:
            self.s.send( pickle.dumps(data) )
            return pickle.loads(self.s.recv(2048*2))
        except socket.error as e:
            print(e)
