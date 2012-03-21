#!/usr/bin/env python2

'''
Created on Mar 20, 2012

@author: mbernt
@version: 0.1
'''
from storageHandler import *
from twitterHelp import *
from addalyse import *
    
def main():
    '''Finds new user to add to database.'''
    twitter_help = TwitterHelp() 
    
    
    while(True):
        # get all all_users from storage handler
        all_users=StorageHandler.get_all_user_names()
        # create a set of users that has already been addalysed
        skip_these_users=set(all_users)
        # for each user add: following and follower
        for user in all_users:
            # get all followers and follows for the user
            #followers_and_following=twitter_help.get_follow_and_followers(user)#need this method
            for f_user in followers_and_following:
                if not (f_user in skip_these_users):
                    skip_these_users.add(f_user)
                    # addalyse
                    addalyse(f_user,-1,True)
                    
            
        #addalyse
        
    

if __name__ == "__main__":
    main()
