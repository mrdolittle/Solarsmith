#!/usr/bin/env python2

'''
Created on Mar 20, 2012

@author: mbernt
@version: 0.1
'''
from storageHandler import *
from twitterHelp import *
from addalyse import *
import time
    
def main():
    '''Finds new user to add to database.'''
    add_latest_tweeters_loop()
    
def add_follow_followers_loop(requests_per_hour = 10):
    '''finds the followers and following of the users in the database and
    addalyses them'''
    twitter_help = TwitterHelp() 
    sleep_time = 3600 / requests_per_hour
    while(True):
        # get all all_users from storage handler
        all_users = StorageHandler.get_all_user_names()
        # create a set of users that has already been addalysed
        skip_these_users = set(all_users)
        # for each user add: following and follower
        for user in all_users:
            # get all followers and follows for the user
            followers_and_following = twitter_help.get_follow_and_followers(user)#TODO: implement in TwitterHelp!
            # can't make to many requests to twitter
            time.sleep(sleep_time)
            for f_user in followers_and_following:
                # don't add already added users
                if not (f_user in skip_these_users):
                    skip_these_users.add(f_user)
                    # addalyse
                    addalyse(f_user,0,True) # TODO: implement in Addalyse!
                    # can't make to many requests to twitter
                    time.sleep(sleep_time)
                    
def add_latest_tweeters_loop(nr_of_latest = 20, requests_per_hour = 10):
    '''Repeatedly tries to add the latest tweeters.'''
    twitter_help = TwitterHelp() 
    sleep_time = 3600 / requests_per_hour
    #skip users that already are in the database
    skip_these_users = set(StorageHandler.get_all_user_names())
    while(True):
        users = twitter_help.get_latest_tweeters(nr_of_latest) # TODO: implement in TwitterHelp!
        # can't make to many requests to twitter
        time.sleep(sleep_time)
        # go through the users list
        for user in users:
            # don't add already added users
            if not (user in skip_these_users):
                # update the skip list
                skip_these_users.add(user)
                # check that the user still isn't in database
                if not StorageHandler.contains(user): # TODO: implement in StorageHandler!
                    # addalyse
                    addalyse(user,0,True) # TODO: implement in Addalyse!
                    # can't make to many requests to twitter
                    time.sleep(sleep_time)
                    
    

if __name__ == "__main__":
    main()
