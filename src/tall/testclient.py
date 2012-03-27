'''
Created on Mar 21, 2012

@author: Jonas & Petter
'''
import httplib
import socket
import urllib


def create_socket(address):
    '''
    Creates a socket for communicating with either storage handler or request.
    '''
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(address)
    soc.sendall('_xantoz_')
    print soc.recv(1024)
    
create_socket(("130.229.178.204", 1337))
