#!/usr/bin/env python2

'''
Created on Mar 20, 2012

TODO: handle exceptions (like when we've been making too many twitter requests sleep for 1 hour in the exception handler)

@author: mbernt, Lucas Taubert
@version: 0.1
'''

import TestHandler
import random
from twitterHelp import *
#from addalyse import *
import time

# TODO: read this from some configuration file in a smart way?
SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"
    
def main():
    '''Finds new user to add to database.'''
    gather_data_loop()
    
    
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
    
    # Initiates the set that will be used for the main loop.
    set_to_add = set([])
    
    # Adds the dummies
    set_to_add.update(set_of_dummies)
    # Adds the publics
    set_to_add.update(set_of_publics)
    
    
    time.sleep(sleep_time)
    
    for s in set_of_publics:
        print s
    
    all_added_users = {}    
    set_to_ignore = load_existing_users()
    set_to_add.difference_update(set_to_ignore)
    #dh = TestHandler()
    #list_to_add = dh.new_users(list_to_add)
    
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
            
def add_follow_followers_loop(requests_per_hour = 10):
    '''Finds the followers and following of the users in the database
    and addalyses them.'''
    '''
    
    twitter_help = TwitterHelp()
    sh = StorageHandler(SOLR_SERVER)
    
    sleep_time = 3600 / requests_per_hour
    
    while(True):
        skip_these_users = set(all_users) # create a set of users that has already been addalysed
        for user in all_users: # for each user add: following and follower

            # get all followers and follows for the user
            followers_and_following = twitter_help.get_follow_and_followers(user) # TODO: implement in TwitterHelp!
            time.sleep(sleep_time) # can't make to many requests to twitter

            for f_user in followers_and_following:
                if not sh.contains(f_user): # don't add already added users
                    addalyse(f_user, 0, True) # TODO: implement in Addalyse!
                    time.sleep(sleep_time) 

'''                    
def add_latest_tweeters_loop(nr_of_latest = 20, requests_per_hour = 10):
    '''Repeatedly tries to add the latest tweeters.'''
    '''
    twitter_help = TwitterHelp() 
    sleep_time = 3600 / requests_per_hour
    
    while(True):
        users = twitter_help.get_latest_tweeters(nr_of_latest) # TODO: implement in TwitterHelp!
        time.sleep(sleep_time) # can't make to many requests to twitter

        for user in users:
            if not sh.contains(user): # don't add already added users
                addalyse(user,0,True) # TODO: implement in Addalyse!
                time.sleep(sleep_time) 
       '''             
    

if __name__ == "__main__":
    main()
