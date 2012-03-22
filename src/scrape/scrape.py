#!/usr/bin/env python2

'''
Created on Mar 20, 2012

TODO: handle exceptions (like when we've been making too many twitter requests sleep for 1 hour in the exception handler)

@author: mbernt, Lucas Taubert
@version: 0.1
'''

import random
from twitterHelp import *
#from addalyse import *
import time

# TODO: read this from some configuration file in a smart way?
SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"
    
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
    return set(['SSDummy_Faye','SSDummy_Burt','SSDummy_Gustavo'])
    
def gather_data_loop(request_per_hour = 30):
    '''Gathers data about twitter IDs, and sends the data to the storage handler.
    '''
    # TODO: Change for real implementation!
    sleep_time = 0 #3600 / request_per_hour
    
    # Defines how many iterations should pass between calls to the storage handler.
    storage_ratio = 10
    
    th = TwitterHelp()
    
    # Initiates the sets which will be used for the searches.
    
    # Adds a dummy set, won't be used in the real implementation.
    set_of_dummies = set(['SSDummy_Janet', 'SSDummy_Henry', 'SSDummy_Hoot', 'SSDummy_Faye', 'SSDummy_Burt', 'SSDummy_Gustavo', 'SSDummy_Amanda', 'SSDummy_Duke', 'SSDummy_Ian', 'SSDummy_Ellen', 'SSDummy_Chrissy'])
    
    # Adds a set from the recent public twitters.
    set_of_publics = th.get_public_twitters()
    
    # Might add the followers of something later...
    #set_of_followers = load_followers(set_of_something)
    
    # Initiates the set that will be used for the main loop.
    set_to_add = set([])
    
    # Adds the dummies
    set_to_add.update(set_of_dummies)
    # Adds the publics
    set_to_add.update(set_of_publics)
    
    
    # Might add the followers of something later...
    time.sleep(sleep_time)
    
    # Might add the followers of something later...
    for s in set_of_publics:
        print s
    
    all_added_users = {}    
    set_to_ignore = load_existing_users()
    set_to_add.difference_update(set_to_ignore)
    
    # Numbers of loops, to track storage ratio.
    loops = 0
    
    # Creates a dictionary for all the users
    user_dict = {}
    for user in set_to_add:
        loops += 1
        data = th.get_all_tweets(user)
        time.sleep(sleep_time)
        print "Adding userdata for " + str(user) + "."
        if not data == None: # Only adds the data if tweets were found.
            user_dict[user] = data
            all_added_users[user] = data
            print "Adding tweets."
        
        if storage_ratio % loops == 0:
            # TODO: Fix!
            # Sends data of the gathered users to the storage handler.
            # addalyse(user_dict)
            # Clears the current dictionary.
            user_dict.clear()
            
    # Foro debugging purposes, displays all users found in this session.
    for key in all_added_users:
        print key + ": "
        for kkey in all_added_users[key]:
            print str(kkey) + ": " + all_added_users[key][kkey]
    

if __name__ == "__main__":
    main()
