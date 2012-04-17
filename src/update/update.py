#!/usr/bin/env python2

'''
Created on Mar 20, 2012

The program that updates users that are already in the database so
that they may be up to date.

TODO: handle exceptions (like when we've been making too many twitter requests sleep for 1 hour in the exception handler)

TODO: WRITE MORE DESCRIPTION OF ME?
'''

from storageHandler import *
from twitterHelp import *
from mx import DateTime as mxDateTime
from logger import logger
import configHandler
import addalyse
import time
import traceback
import sys

#The configuration instance containing the basic configuration methods.
CONFIG = configHandler.Config()
SOLR_SERVER = CONFIG.get_solr_server()

# Every UPDATE_N:th update of a profile do a full analysis throwing away the old one
UPDATE_N = 20

def main():
    '''Gets profiles from storageHandler and checks if they need updating, and if so updates those.'''
    global CONFIG
    
    th = TwitterHelp() 
    sh = StorageHandler(SOLR_SERVER)
    temporarly_ignore_user = {}
    
    sleep_time = 10     # Sleep in seconds per update
    update_time = 1     # Minimum time for a new update (in hours)
    cycle_time = 60*3   # When all users have been checked: sleep
    
    while True:
        #Get the information from Solr
        for (username, since_id, update_count, timestamp) in sh.get_user_fields('*', 'id', 'since_id', 'updatecount', 'timestamp'):
            print("Checking user: " + str(username) + " Last updated: " + str(timestamp)) # Debug print
            
            #Time checks
            current_datetime = mxDateTime.now()
            diff_twitter = current_datetime - timestamp
            if username in temporarly_ignore_user and (current_datetime - temporarly_ignore_user[username]).hours > update_time:
                del temporarly_ignore_user[username]
                
            #If the conditions are met: Continue
            if diff_twitter.hours > update_time and username not in temporarly_ignore_user:     #Continue if it was more than 1 hour ago since the document was updated
                retry = True
                while(retry):
                    print("Updating...")
                    #Try to update:
                    try:
                        addalyse.addalyse(SOLR_SERVER,
                                 username,
                                 since_id,
                                 (update_count % UPDATE_N) == 0,
                                 update_count + 1)
                        retry = False
                    
                    #If the user can no longer be found on Twitter: Remove from Solr
                    except addalyse.AddalyseUserNotOnTwitterError as err:
                        sys.stderr.write("Got: " + str(err) + ". Twitter acount deleted. Deleting from SOLR.\n")
                        sh.delete_ci(username)
                        retry = False
                    
                    #If Solr can not be updated with new Tweet data at the time of the update. Wait for 1h with this user.
                    except addalyse.AddalyseUnableToProcureTweetsError as err:
                        sys.stderr.write(str(err) + "\n")
                        temporarly_ignore_user[username] = mxDateTime.now()
                        retry = False
                    
                    #If the rate limit was exceeded, pause for 1h1min and try again.
                    except addalyse.AddalyseRateLimitExceededError as err:
                        sys.stderr.write("RateLimitExceeded, trying again in 1h")
                        time.sleep(CONFIG.get_rate_limit_exceeded_time())
                        retry = True
                    
                    #If an unhandled exception is found, a traceback will be made so that the programmer can take care of it.
                    except Exception:
                            sys.stderr.write("Unhandled exception:\n")
                            traceback.print_exc()
                            retry = False
                    
                    #Sleep for ten seconds, to not make to many Twitter requests
                    time.sleep(sleep_time)                 
            else:
                print "This user has recently been updated."
        print "Completed one update cycle. Sleeping for " + str(cycle_time) + " seconds."
        time.sleep(cycle_time)       

if __name__ == "__main__":
    main()
