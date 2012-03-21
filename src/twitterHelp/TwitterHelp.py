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
        
    def major_coolness(self):
        return self.twitter_API.GetPublicTimeline()
    
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
        # Unknown error
        return None
    def get_all_tweets(self,username,since_id=None):
        '''Retrieves all tweets from a twitter user.
        @param username: The username of which to find tweets, either ID or alies is accepted.
        @param since_id: [optional] The ID of the earliest tweet that will be included. 
        @return: A list of strings representing tweets, ordered from newest to oldest. None if the user was not found'''
        try:
            statuses = self.twitter_API.GetUserTimeline(username, 1000000, since_id, None)
            a = self.twitter_API
        except twitter.TwitterError:
            return None
        except urllib2.HTTPError:
            return None
        status_strings = []
        for s in statuses:
            status_strings.append(s.text)
        return status_strings

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

     
