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
#from analyse import *

def addalyse(solr_server, username, since_id=0, remake_profile=True, update_count=1):
    '''
    Description:
    Directly returns false if the Twitter user isn't on twitter.
    
    If remakeProfile is true then it will disregard since_id and analyse as many tweets as possible
    and then replace the profile in Solr.
    
    If remakeProfile is false it will analyse tweets newer than since_id and merge the result with the profile in Solr.
    If it exists else add a new profile.
    
    Returns: True if successful else False
    Exceptions: TODO: add them here
    Input types:  addalyse(String solr_server, String username,int since_id,boolean remakeProfile,int update_count):
    Signature:  (boolean succesfull_add) addalyse(String username,int since_id,boolean remake_profile):
    
    Used by: 
    update, scrape and request
    
    Need to access via a connection to:
    twitter_API, sunburnt_API
    '''
    th = TwitterHelp()
    sh = StorageHandler(solr_server)
    
    #remake if not in solr
    remake_profile = remake_profile or not sh.contains(username)
    
    print "addalyse test indata: " + str(tuple([solr_server, username, since_id, remake_profile, update_count]))
    
    if remake_profile:
        # get all tweeets from twitter API 
        tweets = th.get_all_tweets(username, None, True)
        if tweets == None or len(tweets) == 0:
            return False
        # latest tweet is first in list
        new_since_id = tweets[0].id # assumes that the 
        
        # send to analysis
        (lovekeywords, hatekeywords) = ([("cat", 44), ("bear hunting", 22), ("dog", 33)], [("fishing", 55), ("bear grylls", 33)])
        #(lovekeywords, hatekeywords) = analyse.analyse(tweets)# TODO:implement in analyse
        
        # store result in sunburnt
        sh.add_profile(username, lovekeywords, hatekeywords, new_since_id, update_count)
        
        print "add_profile: "+str(sh.get_user_fields(username,'id','since_id','updatecount','lovekeywords_list', 'hatekeywords_list')[0])
        
    else:
        # get tweets newer than sinceID 
        tweets = th.get_all_tweets(username, since_id, True)
        if tweets == None or len(tweets) == 0:
            return False
        
        new_since_id = tweets[0].id
        
        # merging

        # send to analysis
        (lovekeywords, hatekeywords) = ([("cat", 44), ("bear hunting", 22), ("dog", 33)], [("fishing", 55), ("bear grylls", 33)])
        #(lovekeywords, hatekeywords) = analyse.analyse(tweets)# TODO:implement in analyse
        
        # get a users old hatekeywords_list and lovekeywords_list
        doc = sh.get_user_documents(username, 'lovekeywords_list', 'hatekeywords_list')[0]
        
        print "DOC: " + str(doc)
        
        lovekeywords_old = doc.lovekeywords_pylist
        hatekeywords_old = doc.hatekeywords_pylist
        
        print "tar fran solr: " + str(lovekeywords_old) + str(hatekeywords_old)
        
        # merge tuple lists
        lovemerge = merge_tuples(appender(lovekeywords, lovekeywords_old))# gives an exception if lovekeywords==None
        hatemerge = merge_tuples(appender(hatekeywords, hatekeywords_old))
        
        print "lagger in: " + str((lovemerge, hatemerge))
        
        # add merged result to database
        sh.add_profile(username, lovemerge, hatemerge, new_since_id, update_count)
        
        
        
    # returns true if added to database   
    return True 


def appender(list1,list2):
    tmp=[]
    for a in list1:
        tmp.append(a)
    for b in list2:
        tmp.append(b)
    return tmp


def merge_tuples(list_of_only_love_or_only_hate_tuples):
    '''gets a list of love tuples or a list of hate tuple, it merges and adds the values
    of all tuples with the same name. 
    ex [('tjoo',-1),('hi',3),('hi',2),('tjoo',3)] gives [('hi',5),('tjoo',2)]'''
    
    myDict={}
    # merge all tuples with the same keyword and sum the values
    for (keyword,value) in list_of_only_love_or_only_hate_tuples:
        # if exist increment by value  else add (keyword, value)
        myDict [ keyword ] = myDict.get(keyword, 0) + value
    #returns a list of all (key, value) tuples in the dictionary
    return myDict.items()

def test_addalyse():
    print addalyse("http://xantoz.failar.nu:8080/solr/","test", 0, True, 0)
    print addalyse("http://xantoz.failar.nu:8080/solr/","test", 0, False, 0)
    print addalyse("http://xantoz.failar.nu:8080/solr/","jesperannebest", 0, True, 0)
    print addalyse("http://xantoz.failar.nu:8080/solr/","jesperannebest", 0, False, 0)
test_addalyse()
