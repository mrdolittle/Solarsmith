#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
Created on Mar 20, 2012

TODO: handle exceptions (like when we've been making too many twitter requests sleep for 1 hour in the exception handler)

@author: mbernt, Lucas Taubert
@version: 0.1
'''
import argparse

parser = argparse.ArgumentParser(description='A scraper, collecting data from twitter.')
parser.add_argument('-n','--noanalyse', help='If set to "true", skips the analysing part, and prints all twitter data to standard out.', required=False)
args = vars(parser.parse_args())
NO_ANALYSE = False

if args['noanalyse'] == "true":
    NO_ANALYSE = True

if not NO_ANALYSE:
    import addalyse
import twitter
from twitterHelp import TwitterHelp
from storageHandler import StorageHandler
import time
import configHandler
import traceback
import sys

CONFIG = configHandler.Config()
SOLR_SERVER = CONFIG.get_solr_server()


def main():
    '''Finds new user to add to database.'''
    gather_data_loop()
    
def load_followers(users, requests_per_hour=30):
    '''Loads followers to a specified set of users.
    
    @arg users: The users which to find followers for (list/set).
    
    @return: A unique set of users that follows the input users, none
             that was found in the input set.

    TODO: Does not work!! API Support?
    Warning: Many API calls, can take a lot of time!'''
    
    th = TwitterHelp()
    if not NO_ANALYSE:
        sh = StorageHandler(SOLR_SERVER)
    users = set(users);
    new_users = set([]);
    
    for u in users:
        # Does not work (Implement get_followers, change None)
        new_users.update(th.get_followers(None))
    new_users.difference_update(users)
    
    return None
    
    
def load_existing_users():
    '''Loads users from the storage handler, to gain information of
    which users to ignore.
    
    @return: Set containing twitter usernames.'''
    
    #TODO: Implement a real solution, calling the storage handler.
    if not NO_ANALYSE:
        sh = StorageHandler(SOLR_SERVER)
        mset = set([a for (a,) in sh.get_user_fields('*', 'id')])
        print mset
        return mset
    
def gather_data_loop(request_per_hour = 3600, users_to_add = 21, no_analyse=False):
    '''Gathers data about twitter IDs, and sends the data to the
    storage handler.'''
    global CONFIG
    
    # TODO: Change for real implementation!
    sleep_time = 3600 / request_per_hour
    
    th = TwitterHelp()
    if not NO_ANALYSE:
        sh = StorageHandler(SOLR_SERVER)
    
    added_users = 0
    
    # Creates a set for all the users that will be added successfully
    users_added = set()
    
    while(added_users < users_to_add):
        # The set of users which will be added.
        try: 
            set_to_add = th.get_public_tweeters()
        except twitter.TwitterError as err:
            if err.message[0:19] == 'Rate limit exceeded':
                # TODO: optimal version of this would query the twitter api for how long to wait exactly!
                sys.stderr.write("Rate limit exceeded while trying to get public timeline, trying again in "
                                 + str(CONFIG.get_rate_limit_exceeded_time()) + " seconds.\n")
                time.sleep(CONFIG.get_rate_limit_exceeded_time())
            else:
                sys.stderr.write("Got TwitterError while trying to get public timeline " + str(err) + ". Retrying soon.\n")
                traceback.print_exc()
                time.sleep(100)
            continue            # retry the loop
        
        if not NO_ANALYSE:
            print "These will be added:"
            for s in set_to_add:
                print s
        
        for user in set_to_add:
            if NO_ANALYSE:
                tweets = th.get_all_statuses(user)
                print "### NEW USER: " + user
                for t in tweets:
                    try:
                        print t.GetText()
                    except UnicodeEncodeError:
                        continue
                time.sleep(sleep_time)
            else:
                if not sh.contains(user):
                    retry = True     # A retry variable for an inner "goto"
                    while(retry):
                        time.sleep(sleep_time)
                        try:
                            if addalyse.addalyse(SOLR_SERVER, user):
                                users_added.add(user)
                                added_users += 1
                                retry = False
                        except addalyse.AddalyseRateLimitExceededError as err: # Halt for 1 hour if the rate limit is exceeded
                            sys.stderr.write("RateLimitExceeded, trying again in " + str(CONFIG.get_rate_limit_exceeded_time()) + " seconds.\n")
                            time.sleep(CONFIG.get_rate_limit_exceeded_time())
                            retry = True
                        except addalyse.AddalyseError as err: # we use polymorphism here, WEE
                            sys.stderr.write("Addalyse threw an error: "  + str(err) + "\n")
                            retry = False
                        except Exception:
                            # ignore errors non-silently (we print tracebacks!)
                            # TODO: use the logger for this?
                            sys.stderr.write("Unhandled exception\n")
                            traceback.print_exc()
                            retry = False
                    
    # For debugging purposes, displays all users found in this session.
    if not NO_ANALYSE:
        for key in users_added:
            print key + " was added"
            #for key in all_added_users[key]:
            #   print str(kkey) + ": " + all_added_users[key][kkey]
    

if __name__ == "__main__":
    main()
