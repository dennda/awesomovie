import socket
import SocketServer
import threading
import pickle

HOST, PORT = "localhost", 9999

#class MyTCPHandler(SocketServer.BaseRequestHandler):
"""
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
"""




class TCPthreaded(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
        
class TCPEq(SocketServer.BaseRequestHandler):
    #def __init__(self):
    #    pass
    num_frames_method = []
    num_marks_method = []
    retrieve_sample_method = []
    
    @classmethod
    def setFrameMethod(cls, method):
        if type(cls.setFrameMethod) == type(method):
            cls.num_frames_method = method

            
    @classmethod
    def setSelectedMethod(cls, method):
        if type(cls.setSelectedMethod) == type(method):
            cls.num_marks_method = method

    @classmethod
    def setRetrieveMethod(cls, method):
        if type(cls.setRetrieveMethod) == type(method):
            cls.retrieve_sample_method = method
            
    def handle(self):
        print("handling request")
        # self.request is the TCP socket connected to the client
        while True:
            self.data = self.request.recv(1024).strip()
            if self.data[0:5].upper() == "HELLO":
                self.request.send("EHLLO")
            if self.data[0:10].upper() == "NUM_FRAMES":
                if(self.num_frames_method):
                    self.request.send(pickle.dumps(self.num_frames_method()))
                else:
                    print "current frame method not set"
            if self.data[0:9].upper() == "NUM_MARKS":
                if(self.num_marks_method):
                    self.request.send(pickle.dumps(self.num_marks_method()))
            if self.data[0:3].upper() == "GET":
                # format is GET [BOX] [FRAME]
                tab = self.data.split(" ",1)
                print("parsing:" + str(tab[1]))
                print("type:" + str(type(tab[1])))
                tab = pickle.loads(tab[1])
                box = tab[0]
                frame = tab[1]
                #self.request.send("Num marks. box:" + str(box) + "  frame:" + str(frame))
                if(self.retrieve_sample_method):
                    self.request.send(pickle.dumps(self.retrieve_sample_method(box,frame)))
            else:
                print "unknown command from %s :" % self.client_address[0]
                print "DATA START"
                print self.data
                print "DATA END"
                # just send back the same data, but upper-cased
                
            if not self.data: 
                print("CLOSING CONNECTION")
                break

        print("finished handling request")

    @classmethod
    def startServing(cls, hostname, port):
#        self.server = TCPthreaded((hostname, port), TCPEq)
#        self.server_thread = threading.Thread(target=self.server.serve_forever)
#        self.server_thread.setDaemon(True)
#        self.server_thread.start()
        server = TCPthreaded((hostname, port), TCPEq)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        return (server, server_thread)

def bin2num(str, len=2):
    result = 0
    for i in range(0,len):
        result = result <<8
        result = result | ord(str[i])
    return result

def num2bin(num, len=2):
    mask = 0xFF
    result = ''
    for i in range(0,len):
        result = chr(num&mask) +result
        num = num >>8
    return result


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    #server = TCPEq()
    TCPEq.startServing(HOST,PORT)
    
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send('Hello')
    data = s.recv(1024)
    s.send('other data')
    s.send('mroe stuff')
    
    print(data)
    raw_input()

    s.close()
