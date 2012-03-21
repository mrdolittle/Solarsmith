'''
Created on Mar 19, 2012

TODO: WRITE A GOOD DESCRIPTION SDJFJFKJDFKJFDKJDF

@author: mbernt, Xantoz
'''

import sunburnt
from Document import Document


# Globally constanty wierdo thing.
# Should we maybe instead wrap all of this file into a class of some
# sort that takes a solr server in it's constructor?
SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"


def get_all_like_a_crazy_ass_slurper_with_extra_potatomotos():
    '''A crazy function that returns a list of Document:s with all
    fields set according to the result. Still doesn't fetch the
    automatic timestamp of Solrs of when the doc was inserted.

    Don't know if this will actually be used, but it could in fact
    come in handy for instance for updates (instead of the function
    below)

    The crazy name is to emphasize the uncertain future of this
    function (rename it to something sane if we decide to keep it or
    something). '''
    global SOLR_SERVER

    return map(lambda x: Document(x['id'],
                                  x['lovekeywords_list'],
                                  x['hatekeywords_list'],
                                  x['since_id'],
                                  x['updatecount']),
               si.query(id='*').field_limit('id',
                                            'lovekeywords_list',
                                            'hatekeywords_list',
                                            'since_id',
                                            'updatecount').execute())
    

def get_all_user_for_update():
    '''used by update
    //returns: (String username,int sinceid,int updatecount)[] tuples
    returns document[]'''
    global SOLR_SERVER

    si = sunburnt.SolrInterface(SOLR_SERVER)
    return [(x['id'], x['since_id'], x['updatecount'])
            for x in si.query(id='*').field_limit('id', 'since_id', 'updatecount').execute()]




#placeholder
def get_all_user_names():
    '''Queries Solr for all the the twitter user id's currently stored.'''
    global SOLR_SERVER

    # Note: field_limit so we don't get more than neccesary
    # Note: A sunburnt query needs to be executed after it is built
    si = sunburnt.SolrInterface(SOLR_SERVER)
    return [x['id'] for x in si.query(id='*').field_limit('id').execute()]


