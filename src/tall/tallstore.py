# -*- coding: utf-8 -*-
'''
Created on Mar 22, 2012

@author: jonas
'''
import sunburnt
import ast

SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"


def get_list_from_string(string):
    return ast.literal_eval(string)


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
        # Iterate over the list of lovekeyword tuples and throw away the weights.
        for key, _ in lovelist:
            lovekeywords = lovekeywords + [key] # Appends the lovekeywords to a list
        hatekeywords = []
        hatelist = ast.literal_eval(self.hatekeywords_list)
        # Iterate over the list of hatekeyword tuples and throw away the weights.
        for key, _ in hatelist:
            hatekeywords = hatekeywords + [key] # Appends the hatekeywords to a list
        return lovekeywords, hatekeywords
    
    def getId(self):
        '''
        Return the username.
        '''
        return self.id


def get_frienenmies_by_id(username):
    '''Retrieves a users friends and enemies from Solr.'''
    global SOLR_SERVER
    
    interface = sunburnt.SolrInterface(SOLR_SERVER)
    ans = interface.query(id=username)
    for searchee in ans.execute(constructor=SolrUser):
        print "Query executed, result: "
        print searchee
        
    if "searchee" not in locals():
        return False # User is not in Solr
    
    userlovekeywords = get_list_from_string(searchee.lovekeywords_list)
    userhatekeywords = get_list_from_string(searchee.hatekeywords_list)
    print userlovekeywords
    print userhatekeywords
    q = interface.Q
    for key, weight in userlovekeywords:
        q = q | interface.Q(lovekeywords=key) ** int(weight)
    query = interface.query(q)
    for friends in query.execute(constructor=SolrUser):
        print friends
  #  si.query(si.Q(lovekeywords='cat') ** 2.3 | si.Q(lovekeywords='fish') ** 1.2)

#    ans = interface.query(lovekeywords=lovekeywords[0]) # Ska fixas så den inte bara söker på första keyworden
#    loveresult = []
#    for friends in ans.execute(constructor=SolrUser):
#        loveresult = loveresult + [friends]
#    # print loveresult
#    
#    ans = interface.query(lovekeywords=hatekeywords[0])
#    hateresult = []
#    for foes in ans.execute(constructor=SolrUser):
#        hateresult = hateresult + [foes]
#    return (loveresult, hateresult)


#getUserid("xantestuser2")
#friends = interface.query(lovekeywords='Fear')
#for fres in friends.execute(constructor=SolrUser):
#    print fres
