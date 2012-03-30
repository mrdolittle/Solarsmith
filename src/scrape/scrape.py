#!/usr/bin/env python2

'''
Created on Mar 20, 2012

TODO: handle exceptions (like when we've been making too many twitter requests sleep for 1 hour in the exception handler)

@author: mbernt, Lucas Taubert
@version: 0.1
'''

import random
import addalyse
import storageHandler
import urllib2
from twitterHelp import *
#from addalyse import *
import time
import configHandler

CONFIG = configHandler.Config()
SOLR_SERVER = CONFIG.get_solr_server()
    
def main():
    '''Finds new user to add to database.'''
    gather_data_loop()
    
def load_followers(users, requests_per_hour=30):
    '''TODO: Does not work!! API Support?
    Warning: Many API calls, can take a lot of time!
    Loads followers to a specified set of users.
    @arg users: The users which to find followers for (list/set).
    @return: A unique set of users that follows the input users, none that was found in the input set.
    '''
    th = TwitterHelp()
    sh = storageHandler.StorageHandler(SOLR_SERVER)
    
    users = set(users);
    new_users = set([]);
    
    for u in users:
        # Does not work (Implement get_followers, change None)
        new_users.update(th.get_followers(None))
    new_users.difference_update(users)
    
    return None
    
    
def load_existing_users():
    '''Loads users from the storage handler, to gain information of which users to ignore.
    @return: Set containing twitter usernames.
    '''
    #TODO: Implement a real solution, calling the storage handler.
    sh = storageHandler.StorageHandler(SOLR_SERVER)
    mset = set([a for (a,) in sh.get_user_fields('*', 'id')])
    print mset
    return mset
    
def gather_data_loop(request_per_hour = 3600, users_to_add = 21):
    '''Gathers data about twitter IDs, and sends the data to the storage handler.
    '''
    # TODO: Change for real implementation!
    sleep_time = 3600 / request_per_hour
    
    th = TwitterHelp()
    sh = storageHandler.StorageHandler(SOLR_SERVER)
    
    added_users = 0
    
    # Creates a set for all the users that will be added successfully
    users_added = set()
    
    while(added_users < users_to_add):
        # The set of users which will be added.
        set_to_add = th.get_public_twitters()
        
        print "These will be added:"
        for s in set_to_add:
            print s
        
        for user in set_to_add:
            if(not sh.contains(user)):
                time.sleep(sleep_time)
                try:
                    if addalyse.addalyse(SOLR_SERVER, user):
                        users_added.add(user)
                        added_users += 1
                except urllib2.HTTPError:
                    'do nothing'
                
    # For debugging purposes, displays all users found in this session.
    for key in users_added:
        print key + " was added"
        #for kkey in all_added_users[key]:
        #   print str(kkey) + ": " + all_added_users[key][kkey]
    

if __name__ == "__main__":
    main()
