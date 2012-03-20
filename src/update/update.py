'''
Created on Mar 20, 2012

@author: mbernt
'''

from addalyse import *
from storageHandler import *
from twitterHelp import *

def main():
    '''Listens for request and all that jazz. I am a program that
    should run you know. TODO: implement me.'''
    limit=100
    while(True):
        list=StorageHandler.get_all_user_for_update()
        for tuple in list:
            (since_id,update_count,username)=tuple
            #if (since_id!=twitterHelp.get_lates_since_id(username):#check if need updating
            addalyse(username,since_id,update_count>limit)#replace if update_count>limit
        #sleep(1000)
    
if __name__ == "__main__":
    main()