'''
Created on Mar 21, 2012

@author: Jonas & Petter
'''
import httplib
import tallstore

#def client(string):
#    host = httplib.HTTPConnection('localhost', 8001, timeout=10)
#    host.request("GET" + string, 'localhost:8001')
#    print host.getresponse(True).read(None)
#
#print "nagonting"
#client('hej pa servern')

list = tallstore.get_list_from_string("[('cat', 34), ('fishing', 22), ('bear grylls', 33)]")
for temp, asd in list:
    print temp
