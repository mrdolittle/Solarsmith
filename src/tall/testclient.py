'''
Created on Mar 21, 2012

@author: Jonas & Petter
'''
import httplib
import socket
import urllib
from configHandler import configuration

CONFIG = configuration.Config()
REQUEST_HANDLER = CONFIG.get_request_server()

def create_socket(address):
    '''
    Creates a socket for communicating with either storage handler or request.
    '''
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(address)
    soc.sendall('_xantoz_')
    print soc.recv(1024)
    print soc.recv(1024)
    
create_socket((REQUEST_HANDLER, 1337))
