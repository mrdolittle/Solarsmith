'''Created on Mar 20, 2012

@author: Jimmy Larsson'''

#Importing the Twitter library.
import twitter
import urllib2
import re

class TwitterHelp:
    '''TwitterHelp contains the Twitter API as well as 
    custom made functions using the Twitter API.''' 

    def __init__(self):
        # Get us a twitter API instance
        self.twitter_API = twitter.Api()
    
    def twitter_contains(self, username):
        '''checks if a username exists on Twitter.
        @return: True if the user exists, else False'''
        #self.twitter_API.SetCredentials("SSAccount", "ssapiapi")
        try:
            urllib2.urlopen("http://www.twitter.com/" + username)
            # Url was found, the username exists
            return True
        except urllib2.HTTPError as err:
            # Page loading failed
            return False
        except urllib2.URLError as err:
            # Connection failed
            return None
        # Unknown error
        return None
        '''
        try:
            self.twitter_API.GetUserTimeline(username, 0)
            # We seem to have been able to find a user since we could get a timeline
            return True
        except twitter.TwitterError as err:
            if err.message == "Not found":
                # This sort of error message tells us that the user didn't exist
                return False
            else:
                # I don't know what went wrong //Derpy (now it is someone elses problem)
                raise
        
        # If it's a HTTP Error from urrlib2 (404's tend to happen for some reason when using
        # python-twitter-0.6.1 and getting at a non-existent timeline, but not with the newer
        # python-twitter-0.8.2):
        except urllib2.HTTPError:
            print "You seem to be using an old version of python-twitter herp DERP //Xantoz"
            return False
    '''
    def get_all_tweets(self,username):
        '''TODO: Not implemented! 
        A method to get all the tweets from a certain user.'''
        statuses = self.twitter_API.GetUserTimeline(username, None, None, None)
        status_strings = []
        for s in statuses:
            status_strings.append(s.text)
        return status_strings
    
    def get_tweets_since(self,username,since_id):
        '''TODO: Not implemented! 
        A method to get all the tweets from a certain user
        that are newer than the given since_id.'''
        
        return []

    def get_latest_since_ID(self, username):
        '''A method to return the latest since_id value of a certain user.'''

        return self.twitter_API.GetUserTimeline(username, 1)[0].GetId()

     
