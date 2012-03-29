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
    try:
        SOLR_INTERFACE = sunburnt.SolrInterface(SOLR_SERVER)
    except:
        print "Cannot connect to Solr"


def get_common_keywords(userskeywords, otherkeywords):
#    print "other keywords: "
#    print otherkeywords
    commonkeywords = []
    userskeywords_dict = dict(userskeywords)
    for key, weight in otherkeywords:
        if key in userskeywords_dict:
            new_weight = weight + userskeywords_dict[key]
            commonkeywords = commonkeywords + [(key, new_weight)]
    commonkeywords.sort(key=lambda tup: tup[1], reverse=True)
    return commonkeywords


class SolrUser:
    '''
    A class representing a User retrieved from Solr.
    '''
    def __init__(self, id, score, lovekeywords_list, hatekeywords_list, **other_kwargs):
        self.id = id
        self.score = score
        self.lovekeywords_list = ast.literal_eval(lovekeywords_list)
        self.hatekeywords_list = ast.literal_eval(hatekeywords_list)
        self.other_kwargs = other_kwargs

    def __repr__(self):
        return 'Id: %s Score: %s Lovekeywords: %s Hatekeywords: %s' % (self.id, self.score, self.lovekeywords_list, self.hatekeywords_list)

    def get_keywords(self):
        '''
        Get two lists. One with all lovekeywords and one with all hatekeywords.
        None of the lists contain weights.
        '''
        lovekeywords = []
        lovelist = self.lovekeywords_list
        # Iterate over the list of lovekeyword tuples and throw away the weights.
        for key, _ in lovelist:
            lovekeywords = lovekeywords + [key] # Appends the lovekeywords to a list
        hatekeywords = []
        hatelist = self.hatekeywords_list
        # Iterate over the list of hatekeyword tuples and throw away the weights.
        for key, _ in hatelist:
            hatekeywords = hatekeywords + [key] # Appends the hatekeywords to a list
        return lovekeywords, hatekeywords

    def getId(self):
        '''
        Return the username.
        '''
        return self.id
    
    
    def set_lovekeywords(self, lovekeywords):
        self.lovekeywords_list = lovekeywords
        
    
    def set_hatekeywords(self, hatekeywords):
        self.hatekeywords_list = hatekeywords


def get_frienemies_by_id(username):
    '''Retrieves a users friends and enemies from Solr.'''

    query = SOLR_INTERFACE.query(id=username).field_limit(score=True)
    searchee = ''
    try:
        for searchee in query.execute(constructor=SolrUser):
            print "Query executed on username: " + username + ", result: "
            print searchee
        if searchee == '':  # Ändrade kollen, definierade searchee som en tom sträng. searchee existerar inte om användaren inte finns i Solr och man inte definierar den själv
            return False # User is not in Solr
    except:
        return "Error: Connection to Solr lost."
    
    userlovekeywords = searchee.lovekeywords_list
    userhatekeywords = searchee.hatekeywords_list
#    print userlovekeywords
#    print userhatekeywords
    
    query = SOLR_INTERFACE.Q(lovekeywords=userlovekeywords[0][0]) ** userlovekeywords[0][1]
    for keyword, weight in userlovekeywords[1:]:
        query = query | SOLR_INTERFACE.Q(lovekeywords=keyword) ** weight
    for keyword, weight in userhatekeywords:
        query = query | SOLR_INTERFACE.Q(hatekeywords=keyword) ** weight
    try:
        friends = SOLR_INTERFACE.query(query).field_limit(['id', 'lovekeywords_list', 'hatekeywords_list'], score=True).paginate(rows=30).execute(constructor=SolrUser)
    except:
        return "Error: Connection to Solr lost."
#    print "Friends: "
#    print friends

    query = SOLR_INTERFACE.Q(hatekeywords=userlovekeywords[0][0]) ** userlovekeywords[0][1]
    for keyword, weight in userlovekeywords[1:]:
        query = query | SOLR_INTERFACE.Q(hatekeywords=keyword) ** weight
    for keyword, weight in userhatekeywords:
        query = query | SOLR_INTERFACE.Q(lovekeywords=keyword) ** weight
    try:
        enemies = SOLR_INTERFACE.query(query).field_limit(['id', 'lovekeywords_list', 'hatekeywords_list'], score=True).paginate(rows=30).execute(constructor=SolrUser)
    except:
        return "Error: Connection to Solr lost."
#    print "Enemies: "
#    print enemies


    for single_friend in friends:
        common_friend_keywords = get_common_keywords(userlovekeywords, single_friend.lovekeywords_list)
        single_friend.set_lovekeywords(common_friend_keywords) # Set and sort friend lovekeywords to common keywords
        common_friend_keywords = get_common_keywords(userhatekeywords, single_friend.hatekeywords_list)
        single_friend.set_hatekeywords(common_friend_keywords) # Set and sort friend hatekeywords to common keywords
    for single_enemy in enemies:
        common_enemy_keywords = get_common_keywords(userhatekeywords, single_enemy.lovekeywords_list)
        single_enemy.set_lovekeywords(common_enemy_keywords) # Set and sort enemy lovekeywords to common keywords
        common_enemy_keywords = get_common_keywords(userlovekeywords, single_enemy.hatekeywords_list)
        single_enemy.set_hatekeywords(common_enemy_keywords) # Set and sort enemy hatekeywords to common keywords

    userlovekeywords, userhatekeywords = searchee.get_keywords()
    return [friends, enemies, userlovekeywords, userhatekeywords]

def get_frienemies_by_keywords(keywords):
    '''Retrieves a users friends and enemies from Solr.'''
    
    query = SOLR_INTERFACE.Q(lovekeywords=keywords[0])
    for keyword in keywords[1:]:
        query = query | SOLR_INTERFACE.Q(lovekeywords=keyword)
    try:
        friends = SOLR_INTERFACE.query(query).field_limit(['id', 'lovekeywords_list', 'hatekeywords_list'], score=True).paginate(rows=30).execute(constructor=SolrUser)
    except:
        return "Error: Connection to Solr lost."
    query = SOLR_INTERFACE.Q(hatekeywords=keywords[0])
    for keyword in keywords[1:]:
        query = query | SOLR_INTERFACE.Q(hatekeywords=keyword)
    try:
        enemies = SOLR_INTERFACE.query(query).field_limit(['id', 'lovekeywords_list', 'hatekeywords_list'], score=True).paginate(rows=30).execute(constructor=SolrUser)
    except:
        return "Error: Connection to Solr lost."
    return [friends, enemies]
