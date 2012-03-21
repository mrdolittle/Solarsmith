#!/usr/bin/env python2

'''
Created on Mar 20, 2012

The program that updates users that are already in the database so
that they may be up to date.

TODO: WRITE MORE DESCRIPTION OF ME?
'''

from addalyse import *
from storageHandler import *
from twitterHelp import *
import time

def main():
    '''Gets profiles from storageHandler and checks if they need
    updating, and if so updates those.'''
    twitter_help = TwitterHelp() 
    
    # create storageHandler object
    #storage_handler = StorageHandler()
    limit = 100            # do complete update every hundredth update
    while True:
        for (since_id, update_count, username) in get_tuples_info_for_all_users():
            if since_id != twitter_help.get_latest_tweet_id(username): # check if need updating
                addalyse(username,
                         since_id,
                         (update_count % limit) == 0,
                         update_count + 1) 
            time.sleep(10) # sleep for ten seconds, to not make to many requests to twitter
    
if __name__ == "__main__":
    main()
