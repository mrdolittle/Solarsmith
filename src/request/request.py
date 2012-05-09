#!/usr/bin/env python2

'''
Created on Mar 20, 2012

@author: Jimmy Larsson, Lucas Taubert
@version: 0.9

Request will create an instance of the Server class which can be found
in request.py.  The Server will handle the traffic and create threads
accordingly.  For each socket client that connects to the server, the
server will spawn a Client thread.

The Client class is a modification of a normal thread and can also be
found in request.py.  A Client will read the data from the socket and
append the data as well as the client itself, into a list for further
use.

A main thread will continuously check a list to make sure that it is
empty.  If it is not empty, the thread will pop the first element and
process it by sending it through the addalyse package and then expect
an answer. This will be done untill the list is empty again.

TODO: Send another error message for when user doesn't have any tweets
     (similar to user not exists but gui should then inform that no tweets
     exist)

'''

import addalyse 
from twitterHelp import *
from select import *
from sys import *
import threading
import socket
import sys
import traceback
import configHandler
import time

CONFIG = configHandler.Config()
SOLR_SERVER = CONFIG.get_solr_server()
LISTEN = True
CURRENTLY_PROCESSING = ""
        
def add_to_solr(username):
    '''Requests a certain Twitter username to be added.  @argument
    username: A string containing the username of a Twitter user.
    @return: A string "UserAdded" if succesfull, otherwise en error
    message, either: "UserNotOnTwitter" or "OtherError".'''
    
    try:
        addalyse.addalyse(SOLR_SERVER, username)
        return "UserAdded"
    except addalyse.AddalyseUserNotOnTwitterError:
        return "UserNotOnTwitter"
    except addalyse.AddalyseProtectedUserError:
        return "ProtectedUser"
    except addalyse.AddalyseRateLimitExceededError:
        return "RateLimitExceeded"        
    except addalyse.AddalyseUnableToProcureTweetsError as err:
        sys.stderr.write("Couldn't get tweets for some reason:" + str(err) + "\n")
        return "OtherError"
    except Exception:
        sys.stderr.write("Unhandled exception:\n")
        traceback.print_exc()
        return "OtherError"
    return None

    
def main():
    '''The main procedure will create the necessary lists, set up the
    instances and await termination
    '''
    #Create the request list
    request_list = []
    
    #Start the username handler
    username_handle_instance = UsernameHandler(request_list)
    username_handle_instance.start()
    
    #Create a new Server instance
    server_instance = Server(request_list)
    
    #Start listening:
    server_instance.run()
    
class Server():
    '''The server class that handles the incomming connections
    
    @param request_list_input: a request list which is forwarded from
            the main method.  the request list will contain a list of
            usernames requested that they are added into the
            database. This parameter will be sent to each client
            thread that is spawned'''
    
    def __init__(self, request_list_input):
        '''Setting up default variables for the server socket.'''
        
        #Server values
        self.host = ''
        self.port = 1337
        self.server = None
        
        #A list of threads (clients) and the request list
        self.threads = []
        self.request_list = request_list_input
    
    def open_server_socket(self):
        '''Opens a server socket.  On error, the program will exit
        while printing out the error message.'''
        
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)
    
    def run(self):
        '''Listens for incomming connections and creates threads (for
        the clients) accordingly.'''
        
        global LISTEN
        
        #Call the open_server_socket and set start variables.
        self.open_server_socket()
        input = [self.server, sys.stdin]
        
        #Print out console information
        sys.stdout.write("Waiting for connections.\n")
        
        while(LISTEN):
            ready_for_input, ready_for_output, ready_for_except = select(input, [], [])
            for s in ready_for_input:
                #If input comes from a connection:
                if s == self.server:
                    #Create a client on an incoming connection
                    client = Client(self.server.accept(), self.request_list)                    
                    #Print out console information
                    sys.stdout.write("Server: A connection has been established\n")                    
                    #Start the thread
                    client.start()                    
                    #Append the thread to a list of threads
                    self.threads.append(client)                
                #If input comes from the server console:
                elif s == sys.stdin:
                    #Terminate the server
                    sys.stdout.write("Server terminated")
                    LISTEN = False
        #Close down all the threads
        self.server.close()
        for c in self.threads:
            c.join()
                 
class Client(threading.Thread):
    '''The Client class is a modification of a normal thread and can
    be found in request.py.  A Client will read the data from the
    socket and append the data as well as the client itself, into a
    list for further use. The client will also send a response back
    when the received data has been processed.'''
    
    def __init__(self, (client, address), request_list_input):
        '''Used to initiate the values and set the input arguments'''
        
        #Initiate according to the threading.Thread.__init__
        threading.Thread.__init__(self)
        
        #Set the client, address, size and request_list
        self.client = client
        self.address = address
        self.size = 1024
        self.request_list = request_list_input
        
    def run(self):
        '''This method will run continuously until the client is shut
        down or until the terminate command is called upon'''
        #Global currently processing
        global CURRENTLY_PROCESSING
        
        #Set the while parameter
        running = True
        
        while(running):
            #Recieve data through the socket.
            data = self.client.recv(self.size)
            
            #If there is any data:
            if data:                
                #Send the response
                self.client.send("Server response: Received username: " + data)
                if data not in self.request_list and not CURRENTLY_PROCESSING:
                    self.request_list.append((data, self.client))
                else:
                    self.client.send("5") # User already being processed
                    sys.stdout.write("User already being processed.\n")
#            else:
#                #self.client.close()
                running = False
                
class UsernameHandler(threading.Thread):
    '''A class that will handle all of the usernames and their client
    threads and make sure that they are sent and processed one by
    one.'''
    
    def __init__(self, request_list_input):
        '''Initiate the variables used by the UsernameHandler'''
        threading.Thread.__init__(self)
        self.size = 1024
        # self.request_list_empty = True 
        self.request_list = request_list_input
        self.stop_thread = False
        
    def run(self):
        global LISTEN
        global CONFIG
        global CURRENTLY_PROCESSING
        
        #Set the while parameter.
        running = True
        while(running):
            if self.request_list != []:
                data = self.request_list.pop() #data[0] = username, data[1] = socket
                CURRENTLY_PROCESSING = data[0]
                retry = True
                while(retry):
                    sys.stdout.write("Processing username: " + data[0] + "\n")
                    res = add_to_solr(data[0])
                    #On response:
                    if res == "UserAdded":
                        print "UserAdded"
                        data[1].send("1")      #1 = User added
                        retry = False
                    elif res == "UserNotOnTwitter":
                        print "UserNotOnTwitter"
                        data[1].send("2")      #2 = User does not exist on Twitter
                        retry = False
                    elif res == "ProtectedUser":
                        print "ProtectedUser"
                        data[1].send("3")       #3 = Protected User (hidden from public requests)
                        retry = False
                    elif res == "RateLimitExceeded":
                        print "RateLimitExceeded, waiting " + str(CONFIG.get_rate_limit_exceeded_time()) + " seconds.\n"
                        data[1].send("4")       #4 = Other error, send this and wait for 1h1min.
                        time.sleep(CONFIG.get_rate_limit_exceeded_time())
                        retry = True
                    else:
                        print "OtherError"
                        data[1].send("4")       #4 = Other error
                        retry = False
                    #Was the message sent?
    #                if sent == 0:
    #                    raise RuntimeError("Socket connection broken")
    #                else:
                    data[1].close()
                    print "Closed the connection"
            else:
                if not LISTEN:
                    running = False
            time.sleep(0.1)
            
if __name__ == "__main__":
    main()
