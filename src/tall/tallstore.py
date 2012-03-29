# -*- coding: utf-8 -*-
'''
Created on Mar 22, 2012

@author: jonas
'''
import sunburnt
import ast

SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"


def connect_to_solr():
    global SOLR_INTERFACE
    SOLR_INTERFACE = sunburnt.SolrInterface(SOLR_SERVER)


def get_list_from_string(string):
    return ast.literal_eval(string)


class SolrUser:
    '''
    A class representing a User retrieved from Solr.
    '''
    def __init__(self, id, score, lovekeywords_list, hatekeywords_list, **other_kwargs):
        self.id = id
        self.score = score
        self.lovekeywords_list = lovekeywords_list
        self.hatekeywords_list = hatekeywords_list
        self.other_kwargs = other_kwargs

    def __repr__(self):
        return 'Id: %s Score: %s Lovekeywords: %s Hatekeywords: %s' % (self.id, self.score, self.lovekeywords_list, self.hatekeywords_list)

    def get_keywords(self):
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


def get_frienemies_by_id(username):
    '''Retrieves a users friends and enemies from Solr.'''
    query = SOLR_INTERFACE.query(id=username).field_limit(score=True)
    searchee = ''
    for searchee in query.execute(constructor=SolrUser):
        print "Query executed on username: " + username + ", result: "
        print searchee
    if searchee == '':  # Ändrade kollen, definierade searchee som en tom sträng. searchee existerar inte om användaren inte finns i Solr och man inte definierar den själv
        return False # User is not in Solr
    
    userlovekeywords = get_list_from_string(searchee.lovekeywords_list)
    userhatekeywords = get_list_from_string(searchee.hatekeywords_list)
#    print userlovekeywords
#    print userhatekeywords
    
    query = SOLR_INTERFACE.Q(lovekeywords=userlovekeywords[0][0]) ** userlovekeywords[0][1]
    for keyword, weight in userlovekeywords[1:]:
        query = query | SOLR_INTERFACE.Q(lovekeywords=keyword) ** weight
    for keyword, weight in userhatekeywords:
        query = query | SOLR_INTERFACE.Q(hatekeywords=keyword) ** weight
    friends = SOLR_INTERFACE.query(query).field_limit(['id', 'lovekeywords_list', 'hatekeywords_list'], score=True).paginate(rows=30).execute(constructor=SolrUser)
#    print "Friends: "
#    print friends

    query = SOLR_INTERFACE.Q(hatekeywords=userlovekeywords[0][0]) ** userlovekeywords[0][1]
    for keyword, weight in userlovekeywords[1:]:
        query = query | SOLR_INTERFACE.Q(hatekeywords=keyword) ** weight
    for keyword, weight in userhatekeywords:
        query = query | SOLR_INTERFACE.Q(lovekeywords=keyword) ** weight
    enemies = SOLR_INTERFACE.query(query).field_limit(['id', 'lovekeywords_list', 'hatekeywords_list'], score=True).paginate(rows=30).execute(constructor=SolrUser)
#    print "Emenies: "
#    print enemies
    userlovekeywords, userhatekeywords = searchee.get_keywords()
    return [friends, enemies, userlovekeywords, userhatekeywords]

def get_frienemies_by_keywords(keywords):
    '''Retrieves a users friends and enemies from Solr.'''
    
    query = SOLR_INTERFACE.Q(lovekeywords=keywords[0])
    for keyword in keywords[1:]:
        query = query | SOLR_INTERFACE.Q(lovekeywords=keyword)
    friends = SOLR_INTERFACE.query(query).field_limit(['id', 'lovekeywords_list', 'hatekeywords_list'], score=True).paginate(rows=30).execute(constructor=SolrUser)

    query = SOLR_INTERFACE.Q(hatekeywords=keywords[0])
    for keyword in keywords[1:]:
        query = query | SOLR_INTERFACE.Q(hatekeywords=keyword)
    enemies = SOLR_INTERFACE.query(query).field_limit(['id', 'lovekeywords_list', 'hatekeywords_list'], score=True).paginate(rows=30).execute(constructor=SolrUser)

    return [friends, enemies]
