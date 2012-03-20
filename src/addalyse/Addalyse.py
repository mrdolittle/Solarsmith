'''
Created on Mar 19, 2012

@author: mbernt
'''

#from twitterHelp import twitter_help_global
#import addalyse.twitter_help

# global variable
twitter_help=1

def set_globvar():
    # gain access to global variable
    global twitter_help
    # do something
    a=twitter_help

def addalyse(username,since_id,remake_profile):
    '''
    Description:
    Directly returns false if the twitter user isn't on twitter.
    
    if remakeProfile is true then it will disregard sinceID and analyse as many tweets as possible
    and then replace the profile in solr.
    
    if remakeProfile is false it will analyse tweets newer than sinceID and merge the result with the profile in solr
    
    Returns: True if successful else False
    Exceptions:
    Input types:  addalyse(String username,int sinceID,boolean remakeProfile):
    Signature:  (boolean succesfull_add) addalyse(String username,int since_id,boolean remake_profile):
    
    Used by: 
    update, scrape and request
    
    need to access via a connection:
    twitter_API, sunburnt_API
    '''
    # maybe check if the user exists on twitter, but this check might be done in get_all_tweets
    #if !TwitterHelp.contains(username):
    #    return False

    
    if(remake_profile):
        # get all tweeets from twitter API 
        #tweets = TwitterHelp.get_all_tweets(username)
        #if(tweets==None || tweets.length()==0):
        #    return False
        #profile = TwitterHelp.get_profile() #see in solr schema what is needed
        
        # send to analysis
        #analysis=analysis.analyse(tweets)
        
        # store result in sunburnt
        #Storage_handler.add_profile(username,profile,analysis)
        
        return True #returns true if added to solr
    else:
        # get tweets newer than sinceID 
        #tweets = TwitterHelp.get_all_tweets_newer_than(username,sinceID)
        #if(tweets==None || tweets.length()==0):
        #    return False
        
        # send to analysis
        #analysis=analysis.analyse(tweets)
        
        # merge result with the profile in solr
        #Storage_handler.update_profile(username,analysis)
        
        return True # returns true if merged with solr
        
    