'''
Created on Mar 22, 2012

@author: jonas
'''
import sunburnt
import ast

SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"

class SolrUser:
    '''
    A class representing a User retrieved from Solr.
    '''
    def __init__(self, id, lovekeywords_list, hatekeywords_list, **other_kwargs):
        self.lovekeywords_list = lovekeywords_list
        self.id = id
        self.hatekeywords_list = hatekeywords_list
        self.other_kwargs = other_kwargs

    def __repr__(self):
        return 'Id: %s Lovekeywords: %s Hatekeywords: %s' % (self.id, self.lovekeywords_list, self.hatekeywords_list)

    def getKeywords(self):
        '''
        Get two lists. One with all lovekeywords and one with all hatekeywords.
        None of the lists contain weights.
        '''
        lovekeywords = []
        lovelist = ast.literal_eval(self.lovekeywords_list)
        for key, w in lovelist:
#            lovekeywords = lovekeywords + [key + ","]
            lovekeywords = lovekeywords + [key]
        lovekeywords = lovekeywords[:-1]
        hatekeywords = []
        hatelist = ast.literal_eval(self.hatekeywords_list)
        for key, w in hatelist:
#            hatekeywords = hatekeywords + [key + ","]
            hatekeywords = hatekeywords + [key]
        hatekeywords = hatekeywords[:-1]
        return lovekeywords, hatekeywords

    def getId(self):
        '''
        Return the username.
        '''
        return self.id


def get_user_by_id(username):
    '''Retrieves a user from Solr with the specified username.'''
    global SOLR_SERVER
    
    interface = sunburnt.SolrInterface(SOLR_SERVER)
    ans = interface.query(id=username)
    for result in ans.execute(constructor=SolrUser):
        print "Query executed, result: "
        print result
    return result


def get_friends_by_id(username):
    '''Retrieves a users friends and enemies from Solr.'''
    global SOLR_SERVER
    
    # TODO: write function
    interface = sunburnt.SolrInterface(SOLR_SERVER)
    ans = interface.query(id=username)
    for searchee in ans.execute(constructor=SolrUser):
        print "Query executed, result: "
        print searchee

    lovekeywords, hatekeywords = searchee.getKeywords()
#    print "trying to find with two keywords"
    print lovekeywords
    ans = interface.query(lovekeywords=lovekeywords[0])
    result = []
    for friends in ans.execute(constructor=SolrUser):
#        print "get_friends_by_id test: "
        result = result + friends
    return result

get_friends_by_id("xantestuser2")
#getUserid("xantestuser2")
#friends = interface.query(lovekeywords='Fear')
#for fres in friends.execute(constructor=SolrUser):
#    print fres
