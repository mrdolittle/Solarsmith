'''
Created on Mar 20, 2012

@author: Jimmy
@version: 0.1
'''

from addalyse import *

'''
    Requests a certain Twitter username to be added. 
    @argument username: A string containing the username of a Twitter user.
    @return: A boolean set to true if the user has been added, otherwise false.
'''

def request_add(username):
    addalyse(username,0,False)