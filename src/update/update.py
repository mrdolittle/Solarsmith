'''
Created on Mar 20, 2012

@author: mbernt
@version: 0.2
'''

from addalyse import *
from storageHandler import *
from twitterHelp import *

def main():
    '''Gets profiles from storageHandler and checks if they need updating, and if so 
    updates those.'''
    limit=100
    while(True):
        list=StorageHandler.get_all_user_for_update()
        for tuple in list:
            (since_id,update_count,username)=tuple
            #if (since_id!=twitterHelp.get_latest_since_id(username):#check if need updating
            addalyse(username,since_id,update_count>limit)#replace if update_count>limit
        #sleep(1000)
    
if __name__ == "__main__":
    main()