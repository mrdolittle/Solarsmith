# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

'''
Created on Mar 21, 2012

@author: Jonas & Petter
'''
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from xml.sax.saxutils import escape
import select
import socket
import urlparse

import tallstore
import configHandler

CONFIG = configHandler.Config()
REQUEST_SERVER = CONFIG.get_request_server()
REQUEST_SERVER_PORT = 1337
TIMEOUT_FOR_REQUEST = 15
GENERICERROR = "Error: Something went wrong, please try again. If the problem persists, please contact support."


def get_pic_link(username):
    return "https://api.twitter.com/1/users/profile_image/" + str(username)


def create_socket(address):
    '''
    Creates a socket for communicating with either storage handler or request.
    '''
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(address)
    return soc


def send_to_request(username):
    '''
    Sends a username to Request and awaits an answer.
    Returns different values depending on the answer from Request.
    '''
    global REQUEST_SERVER, REQUEST_SERVER_PORT
    print "Trying to connect to request"
    try:
        soc = create_socket((REQUEST_SERVER, REQUEST_SERVER_PORT))
    except:
        print "Error: Cannot connect to request."
        return False, GENERICERROR
    print "Connected"
    try:
        soc.sendall(username)
    except:
        print "Error: Could not send to request."
        return False, GENERICERROR
    print "username sent: " + username
    try:
        ready = select.select([soc], [], [], TIMEOUT_FOR_REQUEST)
        if ready[0]:
            arrived = soc.recv(1024)  # Recieves a response of at most 1k
            print "Arrived to request: " + arrived
        else:
            print "Error: Timeout"
            return (False, GENERICERROR)
        ready = select.select([soc], [], [], TIMEOUT_FOR_REQUEST)
        if ready[0]:
            response = soc.recv(1024)  # Recieves a response of at most 1k
        else:
            print "Error: Timeout"
            return (False, GENERICERROR)
    except:
        print "Error: Could not read from request"
    soc.close()
    if response == "1":
        return (True, "User added, retrieving frienemies.")
        # Anropa storage igen med anvÃ¤ndarnamnet

    elif response == "2":
#        print response
        return (False, "Error: " + username + " does not exist on Twitter. Make sure you spelled it correctly")
        # Tala om fÃ¶r gui att anvÃ¤ndaren inte finns
    elif response == "3":
        # Tala om att anvÃ¤ndaren Ã¤r skyddad
        return (False, "Error: " + username + " has hidden his or her profile, and cannot be shown.")
    elif response == "5":
        # Tala om att användaren redan hanteras
        return (False, "Error: " + username + " is currently being processed, please try again in a minute.")
    else:
        # Response was something else
#        print response
        return (False, GENERICERROR)
        # Tala om fÃ¶r gui att nÃ¥nting pajade

    # 1 = user added
    # 2 = user does not exist
    # 3 = user is hidden
    # 4 = unknown error
    # 5 = user is already being processed by request


def get_and_sort_common_keywords(userskeywords, otherkeywords):
    commonkeywords = []
    for key in otherkeywords:
        if key in userskeywords:
            commonkeywords = commonkeywords + [key]
    return commonkeywords


def create_xml(result):
    '''
    Creates the xml-string that will be sent to the GUI.
    '''
    friendresult, foeresult = result
    # All xml-flags
    searchtag = "<searchResult>"
    friendtag = "<friends>"
    enemiestag = "<enemies>"
    entrytag = "<entry>"
    nametag = "<name>"
    piclinktag = "<piclink>"
    lovekeywordstag = "<lovekeywords>"
    hatekeywordstag = "<hatekeywords>"
    scoretag = "<score>"
    endscoretag = "</score>"
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
        tosend = tosend + entrytag + nametag + escape(friendusername) + endnametag
        tosend = tosend + scoretag + str(friends.score) + endscoretag
        tosend = tosend + piclinktag + escape(get_pic_link(friendusername)) + endpiclinktag
        tosend = tosend + lovekeywordstag

        # Add friend's lovekeywords
        lkw_str = ""
        for keyword in lovekeywords:
            lkw_str = lkw_str + keyword + ","
        lkw_str = escape(lkw_str.rstrip(","))
        tosend = tosend + lkw_str + endlovekeywordstag + hatekeywordstag

        # Add friend's hatekeywords
        hkw_str = ""
        for keyword in hatekeywords:
            hkw_str = hkw_str + keyword + ","
        hkw_str = escape(hkw_str.rstrip(","))
        tosend = tosend + hkw_str + endhatekeywordstag + endentrytag

    # End of friends
    tosend = tosend + endfriendstag

    # Start of foes
    tosend = tosend + enemiestag

    for enemies in foeresult:
        lovekeywords, hatekeywords = enemies.get_keywords()
        enemyusername = enemies.getId()
        # Add a foe
        tosend = tosend + entrytag + nametag + escape(enemyusername) + endnametag
        tosend = tosend + scoretag + str(enemies.score) + endscoretag 
        tosend = tosend + piclinktag + escape(get_pic_link(enemyusername)) + endpiclinktag
        tosend = tosend + lovekeywordstag
        # Add foe's lovekeywords
        lkw_str = ""
        for keyword in lovekeywords:
            lkw_str = lkw_str + keyword + ","
        lkw_str = escape(lkw_str.rstrip(","))
        tosend = tosend + lkw_str + endlovekeywordstag + hatekeywordstag
        # add foe's hatekeywords
        hkw_str = ""
        for keyword in hatekeywords:
            hkw_str = hkw_str + keyword + ","
        hkw_str = escape(hkw_str.rstrip(","))
        tosend = tosend + hkw_str + endhatekeywordstag + endentrytag

    # End of foes
    tosend = tosend + endenemiestag
    # End of Search result
    tosend = tosend + endsearchtag

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
    daemon_threads = True       # Ctrl-C will cleanly kill all spawned threads
    allow_reuse_address = True  # much faster rebinding


class RequestHandler(BaseHTTPRequestHandler):
    '''
    This Handler defines what to do with incoming HTTP requests.
    '''
    def _writexmlheaders(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/xml')
        self.end_headers()

    def _writetextheaders(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_HEAD(self):
        self._writeheaders()

    def send_result(self, result):
        self.wfile.write(result)

    def do_GET(self):
        # KLUDGE: by always reconnecting to Solr we can handle the connection to Solr going down
        # TODO: implement a nicer solution to this by reconnecting only when handling the exception raised when Solr is unreachable
        tallstore.connect_to_solr() 
        
        print self.requestline
        print self.path
        if self.path == "/favicon.ico":
            return
        if self.path == '/':
            return
        command, data = get_arguments(self.path)
#        data = data.lower()
        print "Command: " + command
        print "Data: " + data

        ################
        ######TEST######
        ################
        # ignore anything but the SSDummies
        if command == "testusername":
            frienemy_result = tallstore.get_frienemies_by_id(data, test_mode=True)
            self._writexmlheaders()
            self.send_result(create_xml(frienemy_result))
            return
        ################
        ######TEST######
        ################

        if command == "username":
            data = data.replace('*', '')
            print "new data: " + data
            frienemy_result = tallstore.get_frienemies_by_id(data) # Ska ersÃ¤ttas med anrop till storage handler
            if frienemy_result == False:
                succeeded, message = send_to_request(data)
#                succeeded = False
#                message = "Request is not online. Cannot retrieve new users from Twitter."
#                print message
                print "Succeeded: " + str(succeeded)
                print message
                if succeeded == True:
                    # HÃ¤mta frÃ¥n storage
                    frienemy_result = tallstore.get_frienemies_by_id(data)
                    if frienemy_result == False:
                        return # BÃ¶r ersÃ¤ttas med felkod. Kommer vi hit Ã¤r nÃ¥got allvarligt fel
                else:
                    self._writetextheaders()
                    self.send_result(message)
                    return
        elif command == "keywords":
            data = data.replace('*', ' ')
            keys = data.split(",")
            frienemy_result = tallstore.get_frienemies_by_keywords(keys)
        else:
            self._writetextheaders()
            self.send_result("Error: Bad argument, please verify your input.") 
            return
        if frienemy_result == "Error: Solr connection." or frienemy_result == "Error: Unknown error.":
            self._writetextheaders()
            self.send_result(GENERICERROR)
            return
        self._writexmlheaders()
        self.send_result(create_xml(frienemy_result))



if __name__ == "__main__":        
    # This is for starting the server.
    print "Connecting to Solr"
    tallstore.connect_to_solr()
    serveraddr = ('', 8001)
    srvr = ThreadingServer(serveraddr, RequestHandler)
    print "Server started"
    srvr.serve_forever()
