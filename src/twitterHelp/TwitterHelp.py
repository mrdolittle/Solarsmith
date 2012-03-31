'''Created on Mar 20, 2012

@author: Jimmy Larsson, Lucas Taubert
@version: 0.9dev'''

#Importing the Twitter library.
import twitter
import urllib2
import time
from xml.sax.saxutils import unescape

class TwitterHelp:
    '''TwitterHelp contains the Twitter API as well as 
    custom made functions using the Twitter API.''' 

    def __init__(self):
        # Get us a twitter API instance
        self.twitter_API = twitter.Api()
        self.OAuthTokenString = ""

    def get_screen_name(self, id):
        '''Takes an id and returns a canonical representation of a
        users twitter user id thingamabob potato.'''

        return self.twitter_API.GetUser(id).screen_name
    
    def twitter_contains(self, username):
        '''checks if a username exists on Twitter.
        This method is rather slow, but does _not_ use up any API calls.
        @return: True if the user exists, else False'''
        try:
            urllib2.urlopen("http://www.twitter.com/" + username)
            # Url was found, the username exists
            return True
        except urllib2.HTTPError as err:
            # Page loading failed            
            if err.code == 404:
                return False
            else:
                raise
        except urllib2.URLError:
            # Connection failed
            return None
        # Unknown error # TODO: reraise the exception if we get an
        # error that we don't know how to handle? (or maybe this is
        # already the case since we only match certain types of
        # exceptions here anyhow!)
        return None
    
    def get_public_tweets(self):
        '''Retrieves a dictionary of recent tweets from the public twitter feed.'''
        
        status_dic = {}
        statuses = self.twitter_API.GetPublicTimeline()
        for s in statuses:
            status_dic[s.GetUser().GetScreenName()] = s.text
        return status_dic
        
    
    def get_public_tweeters(self):
        tweets = self.get_public_tweets()
        return set(tweets.keys())
    
    def get_all_statuses(self, username, since_id = None):
        '''Retrieves all tweets from a twitter user and returns them as statuses
        @param  username: The username of which to find tweets, either ID or aliases is accepted
        @param since_id: [optional] The ID of the earliest tweet that will be included
        @return: A list of status objects
        re-throws exceptions from self.twitter_API.GetUserTimeline(id=username, count=200, since_id=since_id) '''
        
        all_statuses = []
        page = 1
        page_ultimate_limit = 3
        view_size = 140
        # get statuses and append to all_statuses
        
        while True:
            print "TwitterHelp.get_all_statuses(): Pulling page", page
            
            retry = True
            while retry:
                try:
                    statuses = self.twitter_API.GetUserTimeline(id=username, count=view_size, since_id=since_id, page=page)
                    retry = False
                except twitter.TwitterError as e:
                    # for anything that isn't capacity error pass it on. For capacity error: try again after sleeping a while
                    if e.message != "Capacity Error":
                        raise
                    print "Got capacity error. Retrying page", page, "for user", username, "in 60 seconds."
                    time.sleep(60)
                        
                    
                    
            if statuses: 
                for status in statuses:
                    status.text = unescape(status.text)
                    all_statuses.append(status)
            else:
                break
            
            # avoid doing an extra call to GetUserTimeline if we already have all tweets 
            if len(statuses) < view_size or page >= page_ultimate_limit: 
                break
            page = page + 1  # next page
            
        return all_statuses    
        
    def get_all_tweets(self, username, since_id=None):
        '''Retrieves all tweets from a twitter user.
        @param username: The username of which to find tweets, either ID or aliases is accepted.
        @param since_id: [optional] The ID of the earliest tweet that will be included. 
        @return: A dictionary containing the tweet IDs mapped to their corresponding tweets in string 
        form. None if the user was not found'''

        statuses = self.get_all_statuses(username, since_id)

        if not statuses:        # handle getting no tweets
            return None

        status_dic = {}
        for s in statuses:
            status_dic[s.id] = s.text
            
        return status_dic

    def get_latest_tweet_id(self, username):
        '''A method to return the id of the latest tweet of a certain user.
        @return: A numerical representation of the ID of a username. None if the user was not found.
        '''
        try:
            return self.twitter_API.GetUserTimeline(username, 1)[0].GetId()
        except twitter.TwitterError:
            return None
        except urllib2.HTTPError:
            return None
    
    def get_followers(self, username, as_pure=False):
        '''TODO: THIS DOES NOT WORK!!
        Returns a set of usernames that follows the specified user.
        @param username: The input username, whom followers will be found for.
        @return: A set of usernames, following the input username.
        '''
        users = self.twitter_API.GetFollowers()
        if as_pure:
            return users
        user_set = set([])
        for u in users:
            user_set.add(u.GetScreenName()) 
        return user_set
            
