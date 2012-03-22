'''
Created on Mar 21, 2012

@author: Jonas & Petter
'''
import httplib


def client(string):
    host = httplib.HTTPConnection('localhost', 8001, timeout=10)
    host.request("GET" + string, 'localhost:8001')
    print host.getresponse(True).read(None)

print "nagonting"
client('hej pa servern')
