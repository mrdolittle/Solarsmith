'''Created on Mar 20, 2012

@author: Jimmy Larsson'''

#Importing the Twitter library.
import twitter
import urllib2

class TwitterHelp:
    '''TwitterHelp contains the Twitter API as well as 
    custom made functions using the Twitter API.''' 

    def __init__(self):
        #declaring the Twitter variables
        self.twitter_API = twitter.Api()
    
    def twitter_contains(self, username):
        '''twitter_contains is used to see if a username exists in the Twitter database.
        @return: True if the user exists, else False'''
        
        try:
            #Catch the result
            self.twitter_API.GetUserTimeline(username, 0)
            return True
        #If an error occured, else raise the exception:
        except twitter.TwitterError as err:
            if err.message == "Not found":
                return False
            else:
                raise
        #If it's a 404 Error (Happens using python-twitter 0.6.1:
        except urllib2.HTTPError:
            return False
    
    def get_all_tweets(self,username):
        '''Not implemented! 
        A method to get all the tweets from a certain user.'''
        return []
    
    def get_tweets_since(self,username,since_id):
        '''Not implemented! 
        A method to get all the tweets from a certain user
        that are newer than the given since_id.'''
        return []

    def get_latest_since_ID(self, username):
        '''A method to return the latest since_ID value of a certain user.'''

        return self.twitter_API.GetUserTimeline(username, 1)[0].GetId()

     