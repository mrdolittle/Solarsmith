#!/usr/bin/env python2.7

'''
Created on Mar 29, 2012

@author: mbernt, anneback
'''

from storageHandler import *
import addalyse
import configHandler
import traceback

CONFIG = configHandler.Config()
SOLR_SERVER = CONFIG.get_solr_server()

def clear_database_and_add_users(usernames=["SSDummy_Janet", "ssdummy_henry", "ssdummy_hoot", "ssdummy_faye"
                                            ,"ssdummy_burt", "ssdummy_gustavo", "ssdummy_amanda"
                                            ,"ssdummy_duke", "ssdummy_ian", "ssdummy_ellen" , "ssdummy_chrissy"], clear=False):
    '''Used by analyse team to test their accuracy!  Removes all users
    from the database and then adds the ones in the usernames list.
    TODO: test it'''
    
    sh = StorageHandler(SOLR_SERVER)
    if clear:
        print "CLEARING DATABASE!"
        sh.delete_all()
    users_left_to_add = len(usernames)
    for username in usernames:
        try:
            print "Adding: " + username + " Left to add: " +str(users_left_to_add)
            users_left_to_add = users_left_to_add - 1
            addalyse.addalyse(sh, username)
        except addalyse.AddalyseError as err:
            sys.stderr.write("Got error from addalyse: " + str(err) : "\n")
        except Exception:
            sys.stderr.write("Unhandled exception\n")
            traceback.print_exc()
            
    print "Done adding test users!"
    
# testing
if __name__ == '__main__':
    clear_database_and_add_users(clear=True)
