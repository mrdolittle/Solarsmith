#!/usr/bin/env python2

'''
Created on Mar 20, 2012

TODO: handle exceptions (like when we've been making too many twitter requests
      respond with an apropriate error message when getting a request)

@author: Jimmy
@version: 0.1
'''

from addalyse import *
from twitterHelp import *

# TODO: read this from some configuration file in a smart way?
SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"

def add_to_solr(username):
    '''Requests a certain Twitter username to be added. 
    @argument username: A string containing the username of a Twitter user.
    @return: A boolean set to true if the user has been added, otherwise false.'''
    
    return addalyse(username,0,True)

    
def main():
    '''Listens for request and all that jazz. I am a program that
    should run you know. TODO: implement me.'''
    th = TwitterHelp()

if __name__ == "__main__":
    main()
    
    
