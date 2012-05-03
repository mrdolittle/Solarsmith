#!/usr/bin/env python2.7

'''
Created on Mar 29, 2012

@author: mbernt, anneback
'''

from storageHandler import StorageHandler
import time
import addalyse
import configHandler
import traceback
import sys

CONFIG = configHandler.Config()
SOLR_SERVER = CONFIG.SOLR_SERVER

def add_users(usernames=["SSDummy_Janet", "ssdummy_henry", "ssdummy_hoot", "ssdummy_faye"
                         ,"ssdummy_burt", "ssdummy_gustavo", "ssdummy_amanda"
                         ,"ssdummy_duke", "ssdummy_ian", "ssdummy_ellen" , "ssdummy_chrissy"],
              clear=False):
    '''Used by analyse team to test their accuracy!  Removes all users
    from the database and then adds the ones in the usernames list.
    TODO: test it'''
    
    sh = StorageHandler(SOLR_SERVER)
    if clear:
        print "CLEARING DATABASE!"
        sh.delete_all()
    users_left_to_add = len(usernames)
    for username in usernames:
        retry = True
        while retry:
            try:
                print "Adding: " + username + " Left to add: " +str(users_left_to_add)
                users_left_to_add = users_left_to_add - 1
                addalyse.addalyse(sh, username)
                retry = False
            except addalyse.AddalyseRateLimitExceededError:
                sys.stderr.write("Rate limit exceeded, waiting " + str(CONFIG.RATE_LIMIT_EXCEEDED_TIME) + " seconds.\n")
                time.sleep(CONFIG.RATE_LIMIT_EXCEEDED_TIME)
                retry = True
            except addalyse.AddalyseError as err:
                sys.stderr.write("Got error from addalyse: " + str(err) + "\n")
                retry = False
            except Exception:
                sys.stderr.write("Unhandled exception\n")
                traceback.print_exc()
                retry = False
            
    print "Done adding test users!"

def redo_all_users():
    print "Redoing all users in Solr like the mythological baws."
    sh = StorageHandler(SOLR_SERVER)
    add_users(map(lambda (a,): a, sh.get_user_fields('*', 'id')))
    
if __name__ == '__main__':
    if 'reanalyse_all_users' in sys.argv[0]:
        redo_all_users()
    else:
        add_users(clear=len(sys.argv) > 1 and sys.argv[1] == 'clear')

