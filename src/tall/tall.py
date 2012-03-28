# -*- coding: utf-8 -*-
'''
Created on Mar 21, 2012

@author: Jonas & Petter
'''
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from xml.dom.minidom import getDOMImplementation
import re
import string
import socket
import tallstore
import urlparse
import xml.dom.minidom
from configHandler import configuration

CONFIG = configuration.Config()
REQUEST_SERVER = CONFIG.get_request_server()
REQUEST_SERVER_PORT = 1337


def get_pic_link(username):
    return "https://api.twitter.com/1/users/profile_image/" + str(username)


def create_socket(address):
    '''
    Creates a socket for communicating with either storage handler or request.
    '''
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(address)
    return soc


## What was this supposed to become? seems irrelevant now /xantoz 
# def send_to_storage(command, data):
#     '''
#     Sends requests to the Storage Handler. What kind of request it is is determined by 'command'.
#     If command is 'username' it requests a list of keywords connected to that username, if it is
#     'keywords' it requests a list of users and the keywords connected to them.
#     '''
#     # TODO: write method to send commands to storage handler
#     print "Command: " + command + " Data: " + data
#     soc = create_socket("localhost:8002")
#     soc.sendall(command)
#     soc.sendall(data)
#     line = soc.recv
#     print line
#     return line


def send_to_request(username):
    '''Sends a username to Request and awaits an answer. Returns different values depending on the 
    answer from Request.'''
    global REQUEST_SERVER, REQUEST_SERVER_PORT
    print "Trying to connect to request"
    soc = create_socket((REQUEST_SERVER, REQUEST_SERVER_PORT))
    print "Connected"
    soc.sendall(username)
    print "username sent: " + username
    response = soc.recv(1024) # Recieves a response of at most 1k
    print "response from request: " + response
    if response == 1:
#        print response
        return (True, "User added, retrieving frienemies.")
        # Anropa storage igen med användarnamnet

    elif response == 2:
#        print response
        return (False, "User does not exist.")
        # Tala om för gui att användaren inte finns
    else:
        # Response was 3 or 4
#        print response
        return (False, "ERROR")
        # Tala om för gui att nånting pajade

    # 1 = user added
    # 2 = user does not exist
    # 3 = timeout
    # 4 = unknown error


def get_common_keywords(userskeywords, otherkeywords):
    commonkeywords = []
    for key in otherkeywords:
        if key in userskeywords:
            commonkeywords = commonkeywords + [key]
    return commonkeywords


def create_xml(result):
    '''
    Creates the xml-string that will be sent to the GUI.
    '''
    friendresult = result[0]
    foeresult = result[1]
    userlovekeywords = result[2]
    if len(result) == 4:
        userhatekeywords = result[3]
    else:
        userhatekeywords = userlovekeywords
    # All xml-flags
    searchtag = "<searchResult>"
    friendtag = "<friends>"
    enemiestag = "<enemies>"
    entrytag = "<entry>"
    nametag = "<name>"
    piclinktag = "<piclink>"
    lovekeywordstag = "<lovekeywords>"
    hatekeywordstag = "<hatekeywords>"
    endpiclinktag = "</piclink>"
    endlovekeywordstag = "</lovekeywords>"
    endhatekeywordstag = "</hatekeywords>"
    endsearchtag = "</searchResult>"
    endfriendstag = "</friends>"
    endenemiestag = "</enemies>"
    endentrytag = "</entry>"
    endnametag = "</name>"
    # Add xml
    tosend = searchtag
    # Add friends
    tosend = tosend + friendtag

    for friends in friendresult:
        lovekeywords, hatekeywords = friends.get_keywords()
        friendusername = friends.getId()
        # Start of friends
        tosend = tosend + entrytag + nametag + friendusername + endnametag
        tosend = tosend + piclinktag + get_pic_link(friendusername) + endpiclinktag
        tosend = tosend + lovekeywordstag

        lovekeywords = get_common_keywords(userlovekeywords, lovekeywords)

        # Add friend's lovekeywords
        for keyword in lovekeywords:
            tosend = tosend + keyword + ","
        tosend = tosend.rstrip(",")
        tosend = tosend + endlovekeywordstag + hatekeywordstag

        hatekeywords = get_common_keywords(userhatekeywords, hatekeywords)

        # Add friend's hatekeywords
        for keyword in hatekeywords:
            tosend = tosend + keyword + ","
        tosend = tosend.rstrip(",")
        tosend = tosend + endhatekeywordstag + endentrytag

    # End of friends
    tosend = tosend + endfriendstag

    # Start of foes
    tosend = tosend + enemiestag

    for enemies in foeresult:
        lovekeywords, hatekeywords = enemies.get_keywords()
        enemyusername = enemies.getId()
        # Add a foe
        tosend = tosend + entrytag + nametag + enemyusername + endnametag
        tosend = tosend + piclinktag + get_pic_link(enemyusername) + endpiclinktag
        lovekeywords = get_common_keywords(userlovekeywords, lovekeywords)
        tosend = tosend + lovekeywordstag
        # Add foe's lovekeywords
        for keyword in lovekeywords:
            tosend = tosend + keyword + ","
        tosend = tosend.rstrip(",")
        tosend = tosend + endlovekeywordstag + hatekeywordstag
        hatekeywords = get_common_keywords(userhatekeywords, hatekeywords)
        # add foe's hatekeywords
        for keyword in hatekeywords:
            tosend = tosend + keyword + ","
        tosend = tosend.rstrip(",")
        tosend = tosend + endhatekeywordstag + endentrytag

    # End of foes
    tosend = tosend + endenemiestag
    # End of Search result
    tosend = tosend + endsearchtag
    # Kanske inte bästa lösningen men den funkar, tar bort tecken som inte gui klarar av
    # Detta är vår blacklist
    tosend = tosend.replace('"', '')
    tosend = tosend.replace('&', '')
    
   
    print "Response: " + tosend

    return tosend.encode('UTF-8')


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
        return command, data
    return "error", "error in arguments"
#    print command
#    print data


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
        self.send_header('Content-type', 'application/xml')
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
        data = data.lower()
        print "Command: " + command
        print "Data: " + data
        if command == "username":
            frienemy_result = tallstore.get_frienemies_by_id(data) # Ska ersättas med anrop till storage handler
            if frienemy_result == False:
                self.send_result('User not found, attempting to add')
#                succeeded, message = send_to_request(data)
                succeeded = False
                message = "Request is not online. Cannot retrieve new users from Twitter."
                if succeeded == True:
                    self.send_result(message)
                    # Hämta från storage
                    frienemy_result = tallstore.get_frienemies_by_id(data)
                    if frienemy_result == False:
                        return # Bör ersättas med felkod. Kommer vi hit är något allvarligt fel
                else:
                    self.send_result(message)
                    return
        elif command == "keywords":
            keys = data.split(",")
            frienemy_result = tallstore.get_frienemies_by_keywords(keys) + [keys]
        else:
            self.send_result("Error: bad argument") 
            return
        self.send_result(create_xml(frienemy_result))


'''
This is for starting the server.
'''
serveraddr = ('', 8001)
srvr = ThreadingServer(serveraddr, RequestHandler)
srvr.serve_forever()
