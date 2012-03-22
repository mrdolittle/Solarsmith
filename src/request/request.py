#!/usr/bin/env python2

'''
Created on Mar 20, 2012

@author: Jimmy Larsson, Lucas Taubert
@version: 0.1
'''

from addalyse import *
from twitterHelp import *
from select import *
from sys import *
import threading
import socket
import sys

def __init__(self):
    '''Setting up default variables for the server socket.'''
    
    self.host = ''
    self.port = 1337
    self.server = None
    self.threads = []
    self.request_list = []
    
def open_server_socket(self):
    '''Opens a server socket. 
        On error, the program will exit while printing out the error message.'''
    try:
        server = socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.host,self.port)
        server.listen(5)
    except socket.error, (value,message):
        if server:
            server.close()
        print "Could not open socket: " + message
        sys.exit(1)

def run(self):
    '''
        Listens for incomming connections and creates threads accordingly.
    '''
    self.open_socket()
    input = [self.server,sys.stdin]
    listen = True
    while(listen):
        ready_for_input,ready_for_except = select(input,[])
        
        for s in ready_for_input:
            #Create a client on an incomming connection
            client = Client(self.server.accept())
            #Start the thread
            client.start()
            #Append the thread to a list of threads
            self.threads.append(client)
        
def add_to_solr(username):
    '''Requests a certain Twitter username to be added. 
    @argument username: A string containing the username of a Twitter user.
    @return: A boolean set to true if the user has been added, otherwise false.'''
    
    return addalyse(username,0,True)

    
def main():
    '''Listens for request and all that jazz. I am a program that
    should run you know. TODO: implement me.'''
    
    #Listen for communication
    start_listening_thread()
    
def start_listening_thread():
    '''TODO: typ d som står i metodnamnet...    
    '''


#if __name__ == "__main__":
#    main()
    
    
class Client(threading.Thread):
    def __init__(self, (client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        
    def run(self):
        running = True
        while(running):
            data = self.client.recv(self.size)
            if data:
                self.client.send(data)
            else:
                self.client.close()
                running = False
                
