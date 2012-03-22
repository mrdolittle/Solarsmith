'''
Created on Mar 21, 2012

@author: Jonas & Petter
'''
import httplib
import urllib


def client(string):
    host = httplib.HTTPConnection('localhost', 8001)
#    urllib.urlretrieve('localhost', None, None, "hej=123")
    host.request("GET", '/?username=xantestuser2')
    print host.getresponse(True).read(None)

print "nagonting"
client('hej pa servern')
