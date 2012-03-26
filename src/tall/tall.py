# -*- coding: utf-8 -*-
'''
Created on Mar 21, 2012

@author: Jonas & Petter
'''
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import socket
import urlparse
import tallstore

def read_line(s):
    '''
    Taken from somewhere, to read a line from a socket.
    ''' 
    ret = ''
    while True:
        c = s.recv(1)
        if c == '\n' or c == '':
            break
        else:
            ret += c
    return ret


def create_socket(address):
    '''
    Creates a socket for communicating with either storage handler or request.
    '''
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(address)
    return soc


def send_to_storage(command, data):
    '''

    '''
    # TODO: write method to send commands to storage handler
    print "Command: " + command + " Data: " + data
    soc = create_socket("localhost:8002")
    soc.sendall(command)
    soc.sendall(data)
    line = read_line(soc)
    print line
    return line


def send_to_request(username):
    '''
    Sends a username to request and awaits an answer.
    '''
    # TODO: write method to send commands to request
    soc = create_socket(("130.229.128.185", 1337))
    soc.sendall(username)
    response = soc.recv(1024)
    
    if response == 1:
        print 1
        return (True, "User added, retrying.")
        # Anropa storage igen med användarnamnet
    
    elif response == 2:
        print 2
        return (False, "User does not exist.")
        # Tala om för gui att användaren inte finns
    elif response == 3 | response == 4:
        print response
        return (False, "ERROR")
        # Tala om för gui att nånting pajade

    # 1 = user added
    # 2 = user does not exist
    # 3 = timeout
    # 4 = unknown error


def create_xml(result):
    '''
    Creates the xml-string that will be sent to the GUI.
    '''
    friendresult, foeresult = result
    # All xml-flags
    xml = "<?xml version 1.0?>"
    searchtag = "<searchResult>"
    friendtag = "<friends>"
    foestag = "<foes>"
    entrytag = "<entry>"
    nametag = "<name>"
    lovekeywordstag = "<lovekeywords>"
    hatekeywordstag = "<hatekeywords>"
    endlovekeywordstag = "</lovekeywords>"
    endhatekeywordstag = "</hatekeywords>"
    endsearchtag = "</searchResult>"
    endfriendstag = "</friends>"
    endfoestag = "</foes>"
    endentrytag = "</entry>"
    endnametag = "</name>"
    # Add xml
    tosend = xml + searchtag
    # Add friends
    tosend = tosend + friendtag

    for friends in friendresult:
        lovekeywords, hatekeywords = friends.getKeywords()
        friendusername = friends.getId()
        # Start of friends
        tosend = tosend + entrytag + nametag + friendusername + endnametag
        tosend = tosend + lovekeywordstag
        
        # Add friend's lovekeywords
        for keyword in lovekeywords:
            tosend = tosend + keyword + ","
        tosend = tosend.rstrip(",")
        tosend = tosend + endlovekeywordstag + hatekeywordstag
        
        # Add friend's hatekeywords
        for keyword in hatekeywords:
            tosend = tosend + keyword + ","
        tosend = tosend.rstrip(",")
        tosend = tosend + endhatekeywordstag + endentrytag

    # End of friends
    tosend = tosend + endfriendstag

    # Start of foes
    tosend = tosend + foestag

    for foes in foeresult:
        lovekeywords, hatekeywords = foes.getKeywords()
        foeusername = foes.getId()
        # Add a foe
        tosend = tosend + entrytag + nametag + foeusername + endnametag
        tosend = tosend + lovekeywordstag
        # Add foe's lovekeywords
        for keyword in lovekeywords:
            tosend = tosend + keyword + ","
        tosend = tosend.rstrip(",")
        tosend = tosend + endlovekeywordstag + hatekeywordstag
        # add foe's hatekeywords
        for keyword in hatekeywords:
            tosend = tosend + keyword + ","
        tosend = tosend.rstrip(",")
        tosend = tosend + endhatekeywordstag + endentrytag

    # End of foes
    tosend = tosend + endfoestag
    # End of Search result
    tosend = tosend + endsearchtag
    print "Response: " + tosend
    return tosend


def get_arguments(path):
    '''
    Retrieves the arguments from the http GET request recieved from the GUI.
    '''
    parsedUrl = urlparse.urlparse(path, 'http', True)
#   print parsedUrl
    arguments = parsedUrl.query
#   print arguments
    splitarguments = arguments.split('&')
#    print splitarguments

    if len(splitarguments) != 1:
        print "more than one argument"
        return
    if splitarguments[0] == '':
        print "argument is null"
        return
    print "correct number of arguments"

    fromgui = splitarguments[0].split('=')
    if len(fromgui) > 1:
        command = fromgui[0]
        data = fromgui[1]
#    print command
#    print data
        return command, data


class ThreadingServer(ThreadingMixIn, HTTPServer):
    '''
    A class for making the server use threads.
    '''
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True


class RequestHandler(BaseHTTPRequestHandler):
    '''
    This Handler defines what to do with incoming HTTP requests.
    '''
    def _writeheaders(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._writeheaders()

    def send_result(self, result):
        self.wfile.write(result)

    def do_GET(self):
        self._writeheaders()
        print self.requestline
        print self.path
        if self.path == "/favicon.ico":
            return
        if self.path == '/':
            return
        command, data = get_arguments(self.path)
        print "Command: " + command
        print "Data: " + data
        frienemy_result = tallstore.get_frienenmies_by_id(data) # Ska ersättas med anrop till storage handler
        if frienemy_result == False:
            self.send_result('User not found, attempting to add')
            succeeded, message = send_to_request(data)
            if succeeded == True:
                self.send_result(message)
                # Hämta från storage
                frienemy_result = tallstore.get_frienenmies_by_id(data)
                if frienemy_result == False:
                    return # Bör ersättas med felkod. Kommer vi hit är något allvarligt fel
            else:
                self.send_result(message)
                return
        self.send_result(create_xml(frienemy_result))
#        result = send_to_storage(command, data)
#        if result == False:
#            send_to_request(data)
#        else:
#            self.send_result("this is our xmlfile")


'''
This is for starting the server.
'''
serveraddr = ('', 8001)
srvr = ThreadingServer(serveraddr, RequestHandler)
srvr.serve_forever()
