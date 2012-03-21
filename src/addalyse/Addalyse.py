'''
Created on Mar 19, 2012

Fetches tweets from Twitter analyses them and executes the order 
if they should be updated or remade in Solr.

Methods: addalyse

Uses: analysis, storageHandler

Used by: request, update, scrape 

@author: mbernt, anneback
'''

#from twitterHelp import twitter_help_global
#import addalyse.twitter_help

from twitterHelp import *
import storageHandler

def addalyse(username, since_id, remake_profile, update_count=0):#,twitter_help=None,sunburnt_API=None):
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
    
    need to access via a connection to:
    twitter_API, sunburnt_API
    '''
    # make a new TwitterHelp object
    twitter_help = TwitterHelp()
    
    # maybe check if the user exists on twitter, but this check might be done in get_all_tweets
    if not twitter_help.contains(username):
        return False

    
    if remake_profile:
        # get all tweeets from twitter API 
        tweets = twitter_help.get_all_tweets(username)
        if tweets == None or tweets.length() == 0:
            return False

        new_since_id = tweets[0].id # latest tweet is first in list
        
        # send to analysis
        (lovekeywords, hatekeywords) = analyse.analyse(tweets)
        
        # store result in sunburnt
        storageHandler.add_profile(username, lovekeywords, hatekeywords, new_since_id, updatecount)
    else:
        # get tweets newer than sinceID 
        tweets = twitter_help.get_tweets_since(username, since_id)
        if tweets == None or tweets.length() == 0:
            return False

        new_since_id = tweets[0].id

        # send to analysis
        (lovekeywords, hatekeywords) = analyse.analyse(tweets)
        
        # merge result with the profile in solr
        # get a users old hatekeywords_list and lovekeywords_list 
        # lovekeywords_old = ?
        # hatekeywords_old = ?
        (lovemerge, hatemerge) = (None, None) # TODO: somehow merge the lovekeywords_old hatekeywords_old with the new ones
        storageHandler.add_profile(username, lovemerge, hatemerge, new_since_id, updatecount)
        
    # returns true if added to database   
    return True 
        
    
