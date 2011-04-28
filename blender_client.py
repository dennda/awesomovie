import socket
import SocketServer
import threading
import pickle

HOST, PORT = "localhost", 9999

def getFrame():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send('NUM_FRAMES')
    data = s.recv(1024)
    s.close()
    return puckle.loads(data.trim())
    
def getBoxCount():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send('NUM_MARKS')
    data = s.recv(1024)
    s.close()
    return puckle.loads(data.trim())

def getSample(box,frame):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send('GET '+ pickle.dumps( (box,frame) ) )
    data = s.recv(1024)
    s.close()
    return puckle.loads(data.trim())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server = TCPEq()
    server.startServing(HOST,PORT)
    
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    s.send('other data')
    s.send('mroe stuff')
    
    print(data)
    input()

    s.close()
