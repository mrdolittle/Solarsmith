'''
Created on Mar 20, 2012

@author: mbernt
@version: 0.2
'''

from addalyse import *
from storageHandler import *
from twitterHelp import *
import time

def main():
    '''Gets profiles from storageHandler and checks if they need updating, and if so 
    updates those.'''
    twitter_help=TwitterHelp()
    limit=100 # do complete update every hundredth update
    while(True):
        list=StorageHandler.get_all_user_for_update()
        for tuple in list:
            (since_id,update_count,username)=tuple
            if since_id!=twitter_help.get_latest_since_id(username):#check if need updating
                addalyse(username,since_id,update_count>limit)#replace if update_count>limit else update
            time.sleep(10)#sleep for ten seconds, to not make to many requests to twitter
    
if __name__ == "__main__":
    main()