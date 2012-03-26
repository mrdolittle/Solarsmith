'''Created on Mar 20, 2012

@author: Jimmy Larsson, Lucas Taubert
@version: 0.9dev'''

#Importing the Twitter library.
import twitter
import urllib2

class TwitterHelp:
    '''TwitterHelp contains the Twitter API as well as 
    custom made functions using the Twitter API.''' 

    def __init__(self):
        # Get us a twitter API instance
        self.twitter_API = twitter.Api()
        self.OAuthTokenString = ""
    
    def twitter_contains(self, username):
        '''checks if a username exists on Twitter.
        This method is rather slow, but does _not_ user up any API calls.
        @return: True if the user exists, else False'''
        #self.twitter_API.SetCredentials("SSAccount", "ssapiapi")
        try:
            urllib2.urlopen("http://www.twitter.com/" + username)
            # Url was found, the username exists
            return True
        except urllib2.HTTPError:
            # Page loading failed
            return False
        except urllib2.URLError:
            # Connection failed
            return None
        # Unknown error # TODO: reraise the exception if we get an error that we don't know how to handle? (or maybe this is already the case since we only match certain types of exceptions here anyhow!)
        return None
    
    def get_public_tweets(self):
        '''Retrieves a dictionary of recent tweets from the public twitter feed.
        '''
        status_dic = {}
        try:
            statuses = self.twitter_API.GetPublicTimeline()
        except twitter.TwitterError:
            return None
        except urllib2.HTTPError:
            return None
        for s in statuses:
            status_dic[s.GetUser().GetScreenName()] = s.text
        return status_dic
        
    
    def get_public_twitters(self):
        tweets = self.get_public_tweets()
        return set(tweets.keys())
    
    def get_all_statuses(self, username, since_id = None):
        '''Retrieves all tweets from a twitter user and returns them as statuses
        @param  username: The username of which to find tweets, either ID or aliases is accepted
        @param since_id: [optional] The ID of the earliest tweet that will be included
        @return: A list of status objects'''
        try:
            return self.twitter_API.GetUserTimeline(username, 1000000, since_id, None)
        except twitter.TwitterError:
            raise #Skickar vidare felet. Kan skicka eget exception om man vill.
        except urllib2.HTTPError:
            raise twitter.TwitterError("Fel i get_all_statuses")
        
    def get_all_tweets(self, username, since_id=None):
        all_added_users = {}
        '''Retrieves all tweets from a twitter user.
        @param username: The username of which to find tweets, either ID or aliases is accepted.
        @param since_id: [optional] The ID of the earliest tweet that will be included. 
        @return: A dictionary containing the tweet IDs mapped to their corresponding tweets in string 
        form. None if the user was not found'''
        status_dic = {}
        try:
            statuses = self.twitter_API.GetUserTimeline(username, 1000000, since_id, None)            
        except twitter.TwitterError:
            return None
        except urllib2.HTTPError:
            return None
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