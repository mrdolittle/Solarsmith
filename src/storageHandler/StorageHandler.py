'''
Created on Mar 19, 2012

TODO: WRITE A GOOD DESCRIPTION SDJFJFKJDFKJFDKJDF

@author: mbernt, Xantoz
'''

import sunburnt
from .Document import Document


class StorageHandler:
    '''TODO: WRITE ME A DESCRIPTION'''

    def __init__(self, solr_server, schema=None):
        '''Pass url to Solr server that the storage handler should connect to.'''
        
        self.si = sunburnt.SolrInterface(solr_server, schema)
        
    def get_user_fields(self, username, *fields):
        """Gets fields on all documents matching the username wildcard.
        username may be either a full username or a wildcard containing: *.
        e.g.: '_xantoz_' '_xan*' or '*'.
        The latter would return all users in Solr.

        Returns the specified fields in a tuple in the same orders as specified.
        
        Example usage:
            (updatecount,) = sh.get_user_fields('someuser', 'updatecount')[0]   # NOTE: single-element tuple is returned so deconstruct it
            (id, since_id) = sh.get_user_fields('someuser', 'id', 'since_id')[0]
            for (a, b, c) in sh.get_user_fields('someuser', 'id', 'since_id', 'updatecount'):
                blah
        """

        return [tuple(map(lambda a: x[a], fields)) for x in self.si.query(id=username).field_limit(fields).execute()]

    def get_user_documents(self, username, *rst):
        """Gets list of documents, represented as Document objects, matching the username wildcard.
        username may be either a full username or a wildcard containing: *.
        e.g.: '_xantoz_' '_xan*' or '*'.
        The latter would return all users in Solr.

        By default returns all fields that would fit in a Document
        object. But if extra arguments are given these are interpreted
        as the fields to actually store in the Document object,
        setting other fields to None."""

        # if extra parameters supplied use those, else use the default of all (relevant) fields
        fields = rst if rst else ['id', 'lovekeywords_list', 'hatekeywords_list', 'since_id', 'updatecount']
        
        return map(lambda x: Document(x['id']                if 'id'                in fields else None,
                                      x['lovekeywords_list'] if 'lovekeywords_list' in fields else None,
                                      x['hatekeywords_list'] if 'hatekeywords_list' in fields else None,
                                      x['since_id']          if 'since_id'          in fields else None,
                                      x['updatecount']       if 'updatecount'       in fields else None),
                   self.si.query(id=username).field_limit(fields).execute())


    def add_profile(self, id, lovekeywords, hatekeywords, since_id, updatecount):
        '''Adds new profile or overrides old one for id in solr'''

        self.si.add(Document(id, lovekeywords, hatekeywords, since_id, updatecount))
        self.si.commit()

    def contains(self, id):
        '''Check if a document known by id is stored in Solr.'''
        
        return self.get_user_fields(id, 'id') != []


    
# old outcommented stuffs 

# # Globally constanty wierdo thing.
# # Should we maybe instead wrap all of this file into a class of some
# # sort that takes a solr server in it's constructor?
# SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"


# def get_all_like_a_crazy_ass_slurper_with_extra_potatomotos():
#     '''A crazy function that returns a list of Document:s with all
#     fields set according to the result. Still doesn't fetch the
#     automatic timestamp of Solrs of when the doc was inserted.

#     Don't know if this will actually be used, but it could in fact
#     come in handy for instance for updates (instead of the function
#     below)

#     The crazy name is to emphasize the uncertain future of this
#     function (rename it to something sane if we decide to keep it or
#     something). '''
#     global SOLR_SERVER


#     si = sunburnt.SolrInterface(SOLR_SERVER)
    

# def get_since_id_and_updatecount_for_all_users():
#     '''Get a tuple list in the following form (String username,num sinceid,num updatecount)[]
#     This method can be used by update.'''
#     global SOLR_SERVER

#     si = sunburnt.SolrInterface(SOLR_SERVER)
#     return [(x['id'], x['since_id'], x['updatecount'])
#             for x in si.query(id='*').field_limit('id', 'since_id', 'updatecount').execute()]


# def get_user_updatecount(user):
#     '''Returns the updatecount stored for one particular user. Returns
#     None if user doesn't exist in Solr.

#     THIS FUNCTION JUST MIGHT END UP BEING UNNECESARY!'''
#     global SOLR_SERVER

#     si = sunburnt.SolrInterface(SOLR_SERVER)
#     result = si.query(id=user).field_limit('updatecount').execute()
#     return None if result == [] else result[0]['updatecount']
    

# #placeholder
# def get_all_user_names():
#     '''Queries Solr for all the the twitter user id's currently stored.'''
#     global SOLR_SERVER

#     # Note: field_limit so we don't get more than neccesary
#     # Note: A sunburnt query needs to be executed after it is built
#     si = sunburnt.SolrInterface(SOLR_SERVER)
#     return [x['id'] for x in si.query(id='*').field_limit('id').execute()]


