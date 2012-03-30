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

CONFIG = configHandler.Config()
SOLR_SERVER = CONFIG.get_solr_server()

# Every UPDATE_N:th update of a profile do a full analysis throwing away the old one
UPDATE_N = 100

def main():
    '''Gets profiles from storageHandler and checks if they need updating, and if so updates those.'''
    
    th = TwitterHelp() 
    sh = StorageHandler(SOLR_SERVER)
    
    sleep_time = 10
    update_time = 1     #Minimum time for a new update (in hours)
    
    while True:
        for (username, since_id, update_count, timestamp) in sh.get_user_fields('*', 'id', 'since_id', 'updatecount', 'timestamp'):
            print("Checking user: " + str(username) + " Last updated: " + str(timestamp)) # Debug print
            current_datetime = mxDateTime.now()
            diff = current_datetime - timestamp
            if diff.hours > update_time:     #Continue if it was more than 1 hour ago since the document was updated
                print("Updating...")
                try:
                    addalyse.addalyse(SOLR_SERVER,
                             username,
                             since_id,
                             (update_count % UPDATE_N) == 0,
                             update_count + 1)
                except addalyse.AddalyseUserNotOnTwitterError as err:
                    sys.stderr.write("Got: " + str(err) + ". Twitter acount deleted. Deleting from database.\n")
                    sh.delete(username)
                except addalyse.AddalyseUnableToProcureTweetsError as err:
                    sys.stderr.write(str(err) + "\n")
                except Exception:
                        sys.stderr.write("Unhandled exception:\n")
                        traceback.print_exc()
                time.sleep(sleep_time) # sleep for ten seconds, to not make to many requests to twitter                
            else:
                print("This user has recently been updated ( " + str(diff.minutes) + " minutes ago).")
       

if __name__ == "__main__":
    main()
