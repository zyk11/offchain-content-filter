#!/usr/bin/python

""" Off-chain content filter API main program """

import datetime, sys, os.path
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

import socket, threading
import matchHash, dbInit

TIME = datetime.datetime.now()

# initializes a threaded socket API to handle multiple requests simultaneously
class threadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(20) # client is disconnected after 20s of inactivity
            threading.Thread(target = self.filterServer,args = (client,address)).start()

    # member function for threaded server, calling matchHashSig() when data is received
    def filterServer(self, client, address):
        size = 102400 #100 KB TX limit
        while True:
            try:
                data = client.recv(size)
                if data:
                    timestamp = TIME.strftime('%Y-%m-%d %HH-%MM-%SS')
                    print('{0} [+] Connected: {1}:{2}'.format(timestamp, address[0], address[1]))
                    # gets image hash and true/false depending on match result
                    imageHash, match = matchHash.matchHashSig(data) 
                    if match: #if True, send True value (1) back to client
                        response = '1'
                        response = response.encode('utf-8')
                        client.send(response)
                        timestamp = TIME.strftime('%Y-%m-%d %HH-%MM-%SS')
                        print ('{0} [!] Illicit content detected - Hash: {1}'.format(timestamp, imageHash))
                else:
                    timestamp = TIME.strftime('%Y-%m-%d %HH-%MM-%SS')
                    raise error('{0} [-] Data receive error: {1}:{2}'.format(timestamp, address[0], address[1]))
            except:
                timestamp = TIME.strftime('%Y-%m-%d %HH-%MM-%SS')
                print ('{0} [-] Disconnected: {1}:{2}'.format(timestamp, address[0], address[1]))
                client.close()
                return False

# initializes the server on the host:port, and creates new thread per connection
def main():

    # initialize DB if not exist
    dbName = 'imageHashList.db'
    if not os.path.exists(dir_path + '/' + dbName):
        timestamp = TIME.strftime('%Y-%m-%d %HH-%MM-%SS')
        print ('{0} [*] Initializing sqlite3 database with images hashes'.format(timestamp))
        dbInit.main()
    # check if socket is available    
    while True:
        port_num = 2222
        host = '127.0.0.1'
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass 
    timestamp = TIME.strftime('%Y-%m-%d %HH-%MM-%SS')
    print ('{0} [*] Listening to incoming connections on {1}:{2}'.format(timestamp, host, port_num))
    #initializes server
    threadedServer(host, port_num).listen()
    
if __name__ == '__main__':
    main()