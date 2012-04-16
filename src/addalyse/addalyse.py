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

import twitter
from twitterHelp import TwitterHelp
from storageHandler import StorageHandler
from analyse import analyse
from operator import itemgetter
import math


KEYWORD_CUTOFF = 1.1            # keywords weighted lower than this will not be included in the final results

class AddalyseError(Exception):
    '''Base class for all variants of errors Addalyse wants to raise.'''
    
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self)[:-1] + repr(self.value) + ')'

class AddalyseUserNotOnTwitterError(AddalyseError): pass
class AddalyseUnableToProcureTweetsError(AddalyseError): pass
class AddalyseProtectedUserError(AddalyseError): pass

def addalyse(*args):
    try:
        return apply(_addalyse, args)
    except twitter.TwitterError as e:
        if e.message == 'Not authorized':
            raise AddalyseProtectedUserError('Not authorized')
        if e.message == "Capacity Error":
            raise AddalyseUnableToProcureTweetsError('Twitter is lazy: Capacity error')
        else:
            raise               # else pass it on
        

def _addalyse(solr_server, username, since_id=0, remake_profile=True, update_count=1):
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

    username = th.get_screen_name(username) # canonicalize the name like a bawz  (in the future, though, th.twitter_contains(sdf) might just return this canonical stuffs)
    
    # solr_server can now optionally be a StorageHandler object
    sh = solr_server if isinstance(solr_server, StorageHandler) else StorageHandler(solr_server)

    # remake if not in Solr
    remake_profile = remake_profile or not sh.contains(username)
    
    if remake_profile:
        # get all tweeets from Twitter API 
        tweets = th.get_all_statuses(username)
        if not tweets: 
            e = AddalyseUnableToProcureTweetsError("I couldn't for the love of me extract some tweets for '" +
                                                   username +
                                                   "'. Maybe they just doesn't have any?")
            e.remake_profile = True
            raise e
        
        # latest tweet is first in lists
        new_since_id = tweets[0].id # assumes that the 
        
        # send to analysis
        print "addalyse(remake_profile=" + str(remake_profile) + "): analyzing, '" + username + "'"
        (lovekeywords, hatekeywords) = filter_analysis(analyse(map(lambda x: x.GetText(), tweets)))
        
        # store result in sunburnt
        print "addalyse(remake_profile=" + str(remake_profile) + "): adding, '" + username + "'"
        sh.add_profile(username, lovekeywords, hatekeywords, new_since_id, update_count)
        print "addalyse(remake_profile=" + str(remake_profile) + "): done"
        
    else:
        tweets = th.get_all_statuses(username, since_id) # get all tweets since since_id
        if not tweets:
            e = AddalyseUnableToProcureTweetsError("I couldn't for the love of me extract some tweets for '" +
                                                   username +
                                                   "'. Maybe they just doesn't have any new ones?")
            e.remake_profile = False
            raise e
           
        new_since_id = tweets[0].id
        
        # MERGING

        # send to analysis
        print "addalyse(remake_profile=" + str(remake_profile) + "): analyzing, '" + username + "'"
        (lovekeywords, hatekeywords) = analyse(map(lambda x: x.GetText(), tweets)) # Don't filter the new analysis just yet, merge it first!
        
        # get a users old hatekeywords_list and lovekeywords_list
        doc = sh.get_user_documents(username, 'lovekeywords_list', 'hatekeywords_list')[0]
        
        lovekeywords_old = doc.lovekeywords_pylist
        hatekeywords_old = doc.hatekeywords_pylist
        
        # merge tuples. Also now that we are done mergeing we can start looking for keywords with a too low weight
        (lovemerge, hatemerge) = filter_analysis((merge_tuples(lovekeywords + lovekeywords_old), merge_tuples(hatekeywords + hatekeywords_old)))
        
        # add merged result to database
        print "addalyse(remake_profile=" + str(remake_profile) + "): adding, '" + username + "'"
        sh.add_profile(username, lovemerge, hatemerge, new_since_id, update_count)
        print "addalyse(remake_profile=" + str(remake_profile) + "): done"
        
    # returns true if added to database   
    return True #TODO: should this return True?
    # return the number of requests to twitter
    #return math.ceil(len(tweets)/140.0)

def merge_tuples(list_of_only_love_or_only_hate_tuples):
    '''Merge all tuples with the same keyword and sum the values.
    
    E.g [('tjoo',1),('hi',3),('hi',2),('tjoo',3)] gives [('hi',5),('tjoo',2)]'''
    
    myDict = {}
    for (keyword,value) in list_of_only_love_or_only_hate_tuples:
        myDict[keyword] = myDict.get(keyword, 0.0) + value         # if exist increment by value else add (keyword, value)
    return myDict.items()                                          # returns a list of all (key, value) tuples in the dictionary


def filter_analysis(lovekeywords_hatekeywords_tuple):
    '''Takes a pair of keyword lists and filters them both for
    keywords with a weight below KEYWORD_CUTOFF. Returns tuple with
    filtered keyword lists.'''
    global KEYWORD_CUTOFF
    
    foo = lambda x: filter(lambda (a,b): b >= KEYWORD_CUTOFF, x)
    return (foo(lovekeywords_hatekeywords_tuple[0]), foo(lovekeywords_hatekeywords_tuple[1]))

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
