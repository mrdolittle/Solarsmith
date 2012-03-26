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
    
    #Start the username handler
    username_handle_instance = UsernameHandler(request_list)
    username_handle_instance.start()

    #Create a new Server instance
    server_instance = Server(request_list)
    
    #Start listening:
    server_instance.run()
    
    #Terminate
    sys.stdout.write("calling the stop_username_handler")
    username_handle_instance.stop_username_handler()
    
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
        #Print out console information
        sys.stdout.write("Waiting for connections.\n")
        while(listen):
            ready_for_input,ready_for_output,ready_for_except = select(input,[],[])
            
            for s in ready_for_input:
                if s == self.server:
                    #Create a client on an incomming connection
                    client = Client(self.server.accept(), self.request_list)
                    #Print out console information
                    sys.stdout.write("Server: A connection has been established\n")
                    #Start the thread
                    client.start()
                    #Append the thread to a list of threads
                    self.threads.append(client)
                elif s == sys.stdin:
                    #Handle the input junk
                    server_input = sys.stdin.readline()
                    sys.stdout.write("Server input: " + server_input)
                    if server_input == "Terminate\n":
                        listen = False
                    if server_input == "Connections\n" and self.threads != []:
                        sys.stdout.write("Found " + str(len(self.threads)) + " active connection(s)!\n")
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
                self.client.send("Server response: Recieved username: " + data)
                if not self.request_list.__contains__(data):
                    self.request_list.append(data)
            else:
                self.client.close()
                running = False
                
class UsernameHandler(threading.Thread):
    '''A class that will handle all of the usernames and make sure that they are
        sent and processed one by one. '''
    
    def __init__(self, request_list_input):
        threading.Thread.__init__(self)
        self.size = 1024
        self.request_list_empty = True 
        self.request_list = request_list_input
        self.stop_thread = False
        
    def run(self):
        running = True
        while(running):
            if self.request_list != []:
                data = self.request_list.pop()
                sys.stdout.write("Processing username: " + data + "\n")
                #TODO: Send to addalyse        
        
if __name__ == "__main__":
    main()