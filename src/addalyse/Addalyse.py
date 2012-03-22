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
from storageHandler import *
from analyse import *

def addalyse(solr_server, username, since_id, remake_profile, update_count=0):#,twitter_help=None,sunburnt_API=None):
    '''
    Description:
    Directly returns false if the twitter user isn't on twitter.
    
    if remakeProfile is true then it will disregard sinceID and analyse as many tweets as possible
    and then replace the profile in solr.
    
    if remakeProfile is false it will analyse tweets newer than sinceID and merge the result with the profile in solr
    
    Returns: True if successful else False
    Exceptions:
    Input types:  addalyse(String solr_server, String username,int sinceID,boolean remakeProfile):
    Signature:  (boolean succesfull_add) addalyse(String username,int since_id,boolean remake_profile):
    
    Used by: 
    update, scrape and request
    
    need to access via a connection to:
    twitter_API, sunburnt_API
    '''
    th = TwitterHelp()
    sh = StorageHandler(solr_server)
    analyser=
    
    # maybe check if the user exists on twitter, but this check might be done in get_all_tweets
    if not th.contains(username):
        return False

    
    if remake_profile:
        # get all tweeets from twitter API 
        tweets = th.get_all_tweets(username)
        if tweets == None or tweets.length() == 0:
            return False

        new_since_id = tweets[0].id # latest tweet is first in list
        
        # send to analysis
        (lovekeywords, hatekeywords) = analyse.analyse(tweets)
        
        # store result in sunburnt
        sh.add_profile(username, lovekeywords, hatekeywords, new_since_id, updatecount)
    else:
        # get tweets newer than sinceID 
        tweets = th.get_tweets_since(username, since_id)
        if tweets == None or tweets.length() == 0:
            return False

        new_since_id = tweets[0].id

        # send to analysis
        (lovekeywords, hatekeywords) = analyse.analyse(tweets)
        
        # merge result with the profile in solr
        # get a users old hatekeywords_list and lovekeywords_list
        doc = sh.get_user_documents(username, 'lovekeywords_list', 'hatekeywords_list')
        (lovekeywords_old, hatekeywords_old) = (doc.lovekeywords_pylist, doc.hatekeywords_pylist) 
        (lovemerge, hatemerge) = (None, None) # TODO: somehow merge the lovekeywords_old hatekeywords_old with the new ones
        sh.add_profile(username, lovemerge, hatemerge, new_since_id, updatecount)
        
        
        
    # returns true if added to database   
    return True 

def analyse_tweets(list_of_tweets):
    '''TODO: finish him!
    calls analyse for all tweets.'''
    mrb=MovieReviewBayes()
    l=[]
    h=[]
    #test
    for tweet in list_of_tweets:
        #test, pretend all words are negative or positive
        # maybe want (word,value)[] where negative values are hate and positive love
        pos_neg=mrb.analyse(tweet)#TODO: test
        (l2, h2)=
        l=l+l2
        h=h+h2
    return (l,h)

def merge_tuples(list_of_only_love_or_only_hate_tuples):
    '''gets a list of love tuples or a list of hate tuple, it merges and adds the values
    of all tuples with the same name. 
    ex [('tjoo',-1),('hi',3),('hi',2),('tjoo',3)] gives [('hi',5),('tjoo',2)]'''
    myDict={}
    for (keyword,value) in list_of_only_love_or_only_hate_tuples:
        if keyword  in myDict:
            myDict[keyword] += value
        else:
            myDict[keyword] = value
    #returns a list of all (key, value) tuples in the dictionary
    return myDict.items()


        
    
