#!/usr/bin/env python2

'''
Created on Mar 20, 2012

TODO: handle exceptions (like when we've been making too many twitter requests sleep for 1 hour in the exception handler)

@author: mbernt
@version: 0.1
'''
from storageHandler import *
from twitterHelp import *
from addalyse import *
import time

# TODO: read this from some configuration file in a smart way?
SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"
    
def main():
    '''Finds new user to add to database.'''
    add_latest_tweeters_loop()
    
def add_follow_followers_loop(requests_per_hour = 10):
    '''Finds the followers and following of the users in the database
    and addalyses them.'''
    
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

                    
def add_latest_tweeters_loop(nr_of_latest = 20, requests_per_hour = 10):
    '''Repeatedly tries to add the latest tweeters.'''
    
    twitter_help = TwitterHelp() 
    sleep_time = 3600 / requests_per_hour
    
    while(True):
        users = twitter_help.get_latest_tweeters(nr_of_latest) # TODO: implement in TwitterHelp!
        time.sleep(sleep_time) # can't make to many requests to twitter

        for user in users:
            if not sh.contains(user): # don't add already added users
                addalyse(user,0,True) # TODO: implement in Addalyse!
                time.sleep(sleep_time) 
                    
    

if __name__ == "__main__":
    main()
