'''
Created on Mar 19, 2012

TODO: WRITE A GOOD DESCRIPTION SDJFJFKJDFKJFDKJDF

@author: mbernt, Xantoz
'''

import sunburnt
from Document import Document

# This is the number of rows we say we want from Solr to somewhat
# approximate "GET ALL THE THINGS" This might be very stupid and we
# might want to instead globally adopt a design (even in the backend
# stuff) that can work using pagination. Be wary of having the
# MAD_LIMIT be too mad and cause the query to explode.
MAD_LIMIT = 1000000000

class StorageHandler:
    '''TODO: WRITE ME A DESCRIPTION'''

    def __init__(self, solr_server, schema=None):
        '''Pass url to Solr server that the storage handler should connect to.'''
        
        self.si = sunburnt.SolrInterface(solr_server, schema)
        
    def get_user_fields(self, username, *fields):
        """Gets fields on all documents matching the username
        wildcard.  username may be either a full username or a
        wildcard containing: *.  However no leading wildcards are
        allowed (refer to sunburnt documentation for instance).
        
        e.g.: '_xantoz_', '_x*z_', '_xan*' or '*'.
              The latter would return all users in Solr.
              However '*toz_' is not a valid wildcard query

        Returns the specified fields in a tuple in the same orders as specified.

        TODO: This method explodes when it tries to get fields not in
              the documents matched or not in the schema or
              whatever. Try to explode nicer? (catch exception; throw
              our own more descriptive one)
        
        Example usage:
            (updatecount,) = sh.get_user_fields('someuser', 'updatecount')[0]   # NOTE: single-element tuple is returned so deconstruct it
            (id, since_id) = sh.get_user_fields('someuser', 'id', 'since_id')[0]
            for (a, b, c) in sh.get_user_fields('someuser', 'id', 'since_id', 'updatecount'):
                blah
        """

        return [tuple(map(lambda a: x[a], fields))
                for x in self.si.query(id=username).field_limit(fields).paginate(rows=MAD_LIMIT).execute()]

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
                   self.si.query(id=username).field_limit(fields).paginate(rows=MAD_LIMIT).execute())


    def add_profile(self, id, lovekeywords, hatekeywords, since_id, updatecount):
        '''Adds new profile or overrides old one for id in solr'''

        self.si.add(Document(id, lovekeywords, hatekeywords, since_id, updatecount))
        self.si.commit()

    def contains(self, id):
        '''Check if a document known by id is stored in Solr.'''
        
        return self.get_user_fields(id, 'id') != []
    
    def get_friends_enemies(self, love_keywords, hate_keywords):
        '''Not implemented!
        returns the tuple (friends, enemies) where friends are a list of usernames sorted on friendliness and
        enemies are a list of usernames sorted on how hate'''
        return ([],[])

    def delete(self, id_or_list_of_id):
        '''Deletes a single document with id id_or_list_of_id if a
        single id is passed. If a list is passed deletes all documents
        with ids in the list id_or_list_of_id.'''

        self.si.delete(id_or_list_of_id)
        self.si.commit()

    def delete_ci(self, id_or_list_of_id):
        '''Similar to regular delete, but also does case insensitive
        matching as well as wildcards.'''

        # We need to match documents with a query to delete case insensitively
        id_list = id_or_list_of_id if isinstance(id_or_list_of_id, list) else [id_or_list_of_id]
        query_list = map(lambda x: self.si.Q(id_ci=x), id_list)

        self.si.delete(queries=query_list)
        self.si.commit()


    def delete_all(self):
        '''BLOWS. UP. EVERYTHING!!!'''

        self.si.delete_all()
        self.si.commit()
