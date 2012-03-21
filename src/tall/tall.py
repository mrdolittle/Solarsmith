# -*- coding: utf-8 -*-
'''
Created on Mar 21, 2012

@author: Jonas & Petter
'''
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import socket
import urlparse


def read_line(s):
    ret = ''

    while True:
        c = s.recv(1)

        if c == '\n' or c == '':
            break
        else:
            ret += c

    return ret


def create_socket(address):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(address)


def send_to_storage(command, data):
    print "Command: " + command + " Data: " + data
    soc = create_socket("localhost:8002")
    soc.sendall(command)
    soc.sendall(data)
    line = read_line(soc)
    print line
    return line


def send_to_request(username):
    soc = create_socket("localhost:8003")
    soc.sendall(username)
    line = read_line(soc)
    print line


def create_xml():
    xml = "<searchResult>\
    <friends>\
    <entry>\
     <name>potatismos</name>\
     <score>123.4</score>\
     <lovekeywords>\
       <keyword name=\"cat\" weight=\"34\" />\
       <keyword name=\"bear grylls\" weight=\"33\" />\
       <keyword name=\"fishing\" weight=\"22\" />\
     </lovekeywords>\
     <hatekeywords>\
       <keyword name=\"car\" weight=\"34\" />\
       <keyword name=\"bike\" weight=\"33\" />\
       <keyword name=\"walking\" weight=\"22\" />\
     </hatekeywords>\
   </entry>\
   <entry>\
     <name>potatismos2</name>\
     <score>123.4</score>\
     <lovekeywords>\
       <keyword name=\"cat\" weight=\"34\" />\
       <keyword name=\"fishing\" weight=\"22\" />\
       <keyword name=\"bear grylls\" weight=\"33\" />\
     </lovekeywords>\
     <hatekeywords>\
       <keyword name=\"cat\" weight=\"34\" />\
       <keyword name=\"fishing\" weight=\"22\" />\
       <keyword name=\"bear grylls\" weight=\"33\" />\
     </hatekeywords>\
   </entry>\
 </friends>\
 <foes>\
    <entry>\
     <name>motatispos</name>\
     <score>1337.2</score>\
     <lovekeywords>\
       <keyword name=\"cat\" weight=\"44\" />\
       <keyword name=\"bear hunting\" weight=\"12\" />\
     </lovekeywords>\
     <hatekeywords>\
       <keyword name=\"cat\" weight=\"44\" />\
       <keyword name=\"bear hunting\" weight=”12” />\
     </hatekeywords>\
   </entry>\
  </foes>\
</searchResult>"
    return xml


def get_arguments(path):
    parsedUrl = urlparse.urlparse(path, 'http', True)
 #   print parsedUrl
    arguments = parsedUrl.query
 #   print arguments
    splitarguments = arguments.split('&')
#    print splitarguments

    if len(splitarguments) != 1:
        print "bigger than 1"
        return
    if splitarguments[0] == '':
        print "null"
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
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True


class RequestHandler(BaseHTTPRequestHandler):
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
        command, data = get_arguments(self.path)
        print "Command: " + command
        print "Data: " + data
        self.send_result(create_xml())
#        result = send_to_storage(command, data)
#        if result == False:
#            send_to_request(data)
#        else:
#            self.send_result("this is our xmlfile")
# main
serveraddr = ('', 8001)
srvr = ThreadingServer(serveraddr, RequestHandler)
srvr.serve_forever()
