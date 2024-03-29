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
parser.add_argument('-l','--localread', help='If filename is specified, reads tweets from that file instead of from  twitter.', required=False)
args = vars(parser.parse_args())
NO_ANALYSE = False

if args['noanalyse'] == "true":
    NO_ANALYSE = True

if not NO_ANALYSE:
    import addalyse
    from analyse import analyse
    from addalyse.addalyse import filter_analysis
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
    if args['localread']:
        scrape_from_file(args['localread'])
    else:
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
                print "#####_NEW_USER_#####"
                print user
                for t in tweets:
                    try:
                        text = t.GetText()
                        print "#####_NEW_TWEET_#####"
                        print text
                        print "#####_END_OF_TWEET_#####"
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

            
def scrape_from_file(filename):
    ''' The main method which will ask for a file to read from, read it, analyse it and store it.
    (Using other methods)'''
    
    print "Filename: " + filename

    #Global variables
    global SOLR_SERVER
    global CONFIG
        
    #What file do you want to read from?
    #file_path = getFile()
    file = open(filename,'r')
    
    #Set the read variables:
    current_user = ""
    tweet_content = []
    in_tweet = False
    
    #Setup the Solr server variable
    solr_server = CONFIG.get_solr_server
    sh = solr_server if isinstance(solr_server, StorageHandler) else StorageHandler(solr_server)
    
    #Start reading the file
    for text in file.readline():
        
        if not "TwitterHelp.get_all_statuses():" in text:
                        
            #Look for a user and store the username in a variable:
            if text == "#####_NEW_USER_#####":
                current_user = file.readline()
                
                #Look for a new Tweet and read till new_user or new_tweet.
            elif text == "#####_NEW_TWEET_#####":
                in_tweet = True
                    
            #Look for the end of a Tweet
            elif text == "#####_END_OF_TWEET_#####":
                in_tweet = False
                if tweet_content != []:
                    #Analyse if there's any content
                    (lovekeywords, hatekeywords) = addalyse(filter_analysis(analyse(tweet_content)))
                    
                    #Store into Solr
                    #parameter 4 = 1, update everything on the next update
                    #parameter 5 = 0, full update on next update
                    sh.add_profile(current_user, lovekeywords, hatekeywords, 1, 0)
                    
                    #Debug print
                    print "Username: " + current_user + " has the following content:\n" + tweet_content
                    print "\n\n The following lovekeywords were found: \n" + lovekeywords
                    print "\n\n The following hatekeywords were found: \n" + hatekeywords
                            
            #Store the content of a Tweet.
            elif in_tweet:
                if text != "":
                    tweet_content.append(text)
                                
def getFile():
    print "Enter the path to the file that you wish to read from:"
    return sys.stdin.readline()
    

if __name__ == "__main__":
    main()

