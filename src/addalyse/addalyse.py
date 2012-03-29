'''
Created on Mar 19, 2012


@author: mbernt, anneback, Xantoz
@version: 1.0

Contains methods for using TwitterHelp, StorageHandler and Analyse to
fetch tweets, analyse them and add them to the database.

Methods: 
addalyse
merge_tuples

Uses: analysis, storageHandler, twitter help
Used by: request, update, scrape 
'''

from twitterHelp import *
from storageHandler import *
from analyse import *
from operator import itemgetter

class AddalyseError(Exception):
    '''Base class for all variants of errors Addalyse wants to raise.'''
    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# subclass of AddalyseError...
class AddalyseUserNotOnTwitterError(AddalyseError): pass
# subclass of AddalyseError...
class AddalyseUnableToProcureTweetsError(AddalyseError): pass

def addalyse(solr_server, username, since_id=0, remake_profile=True, update_count=1):
    '''
    Description:
    If remakeProfile is true then it will disregard since_id and analyse as many tweets as possible
    and then replace the profile in Solr. With only solr_server and username as input this will happen.
    
    If remakeProfile is false it will analyse tweets newer than since_id and if there was a profile in Solr
    merge the result with the profile in Solr, else add a new profile.
    
    Input: 
    @arg solr_server: A String with the address to the Solr server.
    @arg username: A String with the username of the user that is to be analysed.
    @arg since_id: A long that contains the unique id number of the latest analysed tweet of the 
        targeted profile in Solr. This an optional argument which is 0 as default.
    @arg remakeProfile: A boolean which decides if a profile should be updated or remade. Default is True.
    @arg update_count: An int that contains the number of times the profile has only been updated (not remade).
        Default is 1.
    
    Output: No output.
    
    Exceptions: 
    @except AddalyseUserNotOnTwitterError, if the user isn't on Twitter.
    @except AddalyseUnableToProcureTweetsError, if no tweets are returned from Twitter. The cause can be that there are
    no tweets on that user or if remake is false, no new tweets are on Twitter.

    '''
    th = TwitterHelp()
    
    # does not use a Twitter API call
    if not th.twitter_contains(username):
        raise AddalyseUserNotOnTwitterError("Couldn't find any trace of '" + username + "'")
    
    # solr_server can now optionally be a StorageHandler object
    if isinstance(solr_server, StorageHandler):
        sh=solr_server
    else: 
        sh = StorageHandler(solr_server)

    # remake if not in Solr
    remake_profile = remake_profile or not sh.contains(username)
    
    if remake_profile:
        # get all tweeets from Twitter API 
        tweets = th.get_all_statuses(username)
        if not tweets: 
            e = AddalyseUnableToProcureTweetsError("I couldn't for the love of me extract some tweets for '" +
                                                   username +
                                                   "'. Maybe he just doesn't have any?")
            e.remake_profile = True
            raise e
        
        # latest tweet is first in lists
        new_since_id = tweets[0].id # assumes that the 
        
        # send to analysis
        #(lovekeywords, hatekeywords) = ([("cat", 44), ("bear hunting", 22), ("dog", 33)], [("fishing", 55), ("bear grylls", 33)])
        (lovekeywords, hatekeywords) = compiler.analyse(map(lambda x: x.GetText(), tweets))# TODO:implement in analyse
        
        # store result in sunburnt
        sh.add_profile(username, lovekeywords, hatekeywords, new_since_id, update_count)
        
    else:
        tweets = th.get_all_statuses(username, since_id) # get all tweets since since_id
        if not tweets:
            e = AddalyseUnableToProcureTweetsError("I couldn't for the love of me extract some tweets for '" +
                                                   username +
                                                   "'. Maybe he just doesn't have any new ones?")
            e.remake_profile = False
            raise e
           
        new_since_id = tweets[0].id
        
        # MERGING

        # send to analysis
        #(lovekeywords, hatekeywords) = ([("cat", 44), ("bear hunting", 22), ("dog", 33)], [("fishing", 55), ("bear grylls", 33)])
        (lovekeywords, hatekeywords) = compiler.analyse(map(lambda x: x.GetText(), tweets))

        
        # get a users old hatekeywords_list and lovekeywords_list
        doc = sh.get_user_documents(username, 'lovekeywords_list', 'hatekeywords_list')[0]
        
        lovekeywords_old = doc.lovekeywords_pylist
        hatekeywords_old = doc.hatekeywords_pylist
        
        # merge tuples
        lovemerge = merge_tuples(lovekeywords + lovekeywords_old)# gives an exception if lovekeywords==None
        hatemerge = merge_tuples(hatekeywords + hatekeywords_old)
        
        # add merged result to database
        sh.add_profile(username, lovemerge, hatemerge, new_since_id, update_count)    
        
    # returns true if added to database   
    return True #TODO: should this return True?

def merge_tuples(list_of_only_love_or_only_hate_tuples):
    '''Gets a list of love tuples or a list of hate tuples, it merges
    and adds the values of all tuples with the same name.
    
    E.g [('tjoo',1),('hi',3),('hi',2),('tjoo',3)] gives [('hi',5),('tjoo',2)]'''
    
    myDict = {}
    # merge all tuples with the same keyword and sum the values
    for (keyword,value) in list_of_only_love_or_only_hate_tuples:
        # if exist increment by value else add (keyword, value)
        myDict[keyword] = myDict.get(keyword, 0.0) + value
    # returns a list of all (key, value) tuples in the dictionary
    return myDict.items()



# TEST
def unduplicate_and_sort_tweets(old_tweets, new_tweets):
    '''Untested! Not working?
    Returns a list of tweets (from old_tweets and new_tweets) with duplicates 
    removed and then sorted on since_id.
    Can be used when storing tweets in Solr.'''
    # add them to one list
    tweets=new_tweets+old_tweets
    # remove duplicates
    d={}.fromkeys(tweets,None)
    # get list from d
    tweets=d.keys()
    # sort the tweets on since id, (Not working! want to get since_id with itemgetter)
    tweets=sorted(tweets,key=itemgetter('since_id'))
    # return sorted tweets list
    return tweets

#def test_addalyse():
#    print addalyse("http://xantoz.failar.nu:8080/solr/","test", 0, True, 0)
#    print addalyse("http://xantoz.failar.nu:8080/solr/","test", 0, False, 0)
#    print addalyse("http://xantoz.failar.nu:8080/solr/","jesperannebest", 0, True, 0)
#    print addalyse("http://xantoz.failar.nu:8080/solr/","jesperannebest", 0, False, 0)
# test_addalyse()
