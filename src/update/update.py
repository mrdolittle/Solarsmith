#!/usr/bin/env python2

'''
Created on Mar 20, 2012

The program that updates users that are already in the database so
that they may be up to date.

TODO: handle exceptions (like when we've been making too many twitter requests sleep for 1 hour in the exception handler)

TODO: WRITE MORE DESCRIPTION OF ME?
'''

from addalyse import *
from storageHandler import *
from twitterHelp import *
import time

# TODO: read this from some configuration file in a smart way?
SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"

# Every UPDATE_N:th update of a profile do a full analysis throwing away the old one
UPDATE_N = 100

def main():
    #only_update_loop() # alt1
    update_and_repair_loop() # alt2
    
    
def only_update_loop():
    '''alt1. Gets profiles from storageHandler and checks if they need updating, and if so updates those.'''
    
    th = TwitterHelp() 
    sh = StorageHandler(SOLR_SERVER)
    
    sleep_time=10
    
    while True:
        for (username, since_id, update_count, timestamp) in sh.get_user_fields('*', 'id', 'since_id', 'updatecount', 'timestamp'):
            print("updating user " + str(username) + " last updated " + str(timestamp)) # Debug printage
            # TODO: use timestamp to check if already updated updated today (or something like that)
            #       and then choose to not update. (timestamp is automatically generated by solr when adding/updateing a profile)
            if since_id != th.get_latest_tweet_id(username): # check if need updating
                addalyse(SOLR_SERVER,
                         username,
                         since_id,
                         (update_count % UPDATE_N) == 0,
                         update_count + 1) 
            time.sleep(sleep_time) # sleep for ten seconds, to not make to many requests to twitter
    

def update_and_repair_loop():
    '''alt2. Gets profiles from storageHandler and checks if they need updating, and if so updates those.
    always updates if fields in the database are missing.'''
    
    th = TwitterHelp() 
    sh = StorageHandler(SOLR_SERVER)
    
    sleep_time=1
    
    fields=['id', 'since_id', 'updatecount', 'timestamp']
    
    while True:
        for dct in sh.try_get_user_fields_as_dicts('*', fields):
            update = False;
            (username,since_id,update_count)=(dct[fields[0]], dict.get(fields[1],-1), dct.get(fields[2],-1))
            if since_id == -1 or update_count == -1:# set the missing values and set update to true
                print "Fixing error in database..."
                update_count = 0
                since_id = 0
                update = True
            else: 
                # TODO: use timestamp to check if already updated updated today (or something like that)
                # and then choose to not update. (timestamp is automatically generated by solr when adding/updateing a profile)
                if since_id != th.get_latest_tweet_id(username):
                    update = True
                time.sleep(sleep_time) # sleep for ten seconds, to not make to many requests to twitter
            if update:
                addalyse(SOLR_SERVER,
                         username,
                         since_id,
                         (update_count % UPDATE_N) == 0,
                         update_count + 1) 
                time.sleep(sleep_time) # sleep for ten seconds, to not make to many requests to twitter
                
            
    
if __name__ == "__main__":
    main()
