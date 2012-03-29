'''
Created on Mar 29, 2012

@author: mbernt, anneback
'''

from storageHandler import *
from addalyse import *

# TODO: read this from some configuration file in a smart way?
SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"

def clear_database_and_add_users(usernames=["SSDummy_Janet", "ssdummy_henry", "ssdummy_hoot", "ssdummy_faye"
                                            ,"ssdummy_burt", "ssdummy_gustavo", "ssdummy_amanda"
                                            ,"ssdummy_duke", "ssdummy_ian", "ssdummy_ellen" , "ssdummy_chrissy"]):
    
    '''Used by analyse team to test their accuracy!
    Removes all users from the database and then adds the ones in the usernames list.
    TODO: test it'''
    sh = StorageHandler(SOLR_SERVER)
    sh.delete_all()
    users_left_to_add = len(usernames)
    print "CLEARING DATABASE!"
    for username in usernames:
        print "Adding: " + username + " Left to add: " +str(users_left_to_add)
        try:
            users_left_to_add = users_left_to_add - 1
            addalyse(sh,username)
        except Exception,e:
            print e
    print "Done adding test users!"
    
# testing
clear_database_and_add_users()