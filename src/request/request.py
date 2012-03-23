#!/usr/bin/env python2

'''
Created on Mar 20, 2012

@author: Jimmy Larsson, Lucas Taubert
@version: 0.1
'''

#from addalyse import *
from twitterHelp import *
from select import *
from sys import *
import threading
import socket
import sys
        
def add_to_solr(username):
    '''Requests a certain Twitter username to be added. 
    @argument username: A string containing the username of a Twitter user.
    @return: A boolean set to true if the user has been added, otherwise false.'''
    
    #return addalyse(username,0,True)

    
def main():
    '''Start up the server instance'''
    #Create the request list
    request_list = []
    
    #Create a new Server instance
    server_instance = Server(request_list)
    
    #Start listening:
    server_instance.run()

    if request_list != []:
        for e in request_list:
            sys.stdout.write(request_list[e])
    else:
        sys.stdout.write("Request list was empty. Program now shutting down.")
class Server():
    '''The server that handles the incomming connections'''
    
    def __init__(self, request_list_input):
        '''Setting up default variables for the server socket.'''
        
        self.host = ''
        self.port = 1337
        self.server = None
        self.threads = []
        self.request_list = request_list_input
    
    def open_server_socket(self):
        '''Opens a server socket. 
           On error, the program will exit while printing out the error message.'''
        
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)
    
    def run(self):
        '''Listens for incomming connections and creates threads accordingly.'''
        
        self.open_server_socket()
        input = [self.server,sys.stdin]
        listen = True
        while(listen):
            ready_for_input,ready_for_output,ready_for_except = select(input,[],[])
            
            for s in ready_for_input:
                if s == self.server:
                    #Create a client on an incomming connection
                    client = Client(self.server.accept(), self.request_list)
                    #Start the thread
                    client.start()
                    #Append the thread to a list of threads
                    self.threads.append(client)
                    sys.stdout.write("New socket accepted!\n")
                elif s == sys.stdin:
                    #Handle the input junk
                    server_input = sys.stdin.readline()
                    sys.stdout.write("Server input: " + server_input)
                    if server_input == "Terminate\n":
                        listen = False
                    if server_input == "Connections\n" and self.threads != []:
                        sys.stdout.write("Connection found " + str(len(self.threads)) + " connections!\n")
                    if server_input == "Connections\n" and self.threads == []:
                        sys.stdout.write("Currently there are no active threads \n")
                    
        
        #Close down all the threads
        self.server.close()
        for c in self.threads:
            c.join()
                 
class Client(threading.Thread):
    def __init__(self, (client,address), request_list_input):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.request_list = request_list_input
        
    def run(self):
        running = True
        while(running):
            data = self.client.recv(self.size)
            if data:
                sys.stdout.write("Recieved username: " + data)
                self.client.send("Recieved username: " + data)
                if not self.request_list.__contains__(data):
                    self.request_list.append(data)
            else:
                self.client.close()
                running = False
                
#class UsernameHandler:
    
if __name__ == "__main__":
    main()