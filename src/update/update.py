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
    limit = 100            # do complete update every hundredth update
    while(True):
        list = StorageHandler.get_all_user_for_update()
        for (since_id, update_count, username) in list:
            if since_id != twitter_help.get_latest_since_id(username): # check if need updating
                addalyse(username, since_id, update_count > limit) # replace if update_count>limit else update
            time.sleep(10) # sleep for ten seconds, to not make to many requests to twitter
    
if __name__ == "__main__":
    main()
