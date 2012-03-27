'''
Module for the eminent class Document
'''

import ast


def weight_total(lst):
    '''Returns the total weight of a list of (keyword, weight) tuples.'''
    return sum(map(lambda x: x[1], lst))

def scale_keyword_list(lst):
    '''Scale list of (keyword, weight) pairs so that the weight will
    be scaled to the interval 0.0 to 1.0 inclusive, that is the
    weights will be relative.'''

    if not lst:
        return []
    
    scale = weight_total(lst)
    return map(lambda (a,b): (a, float(b)/scale), lst)

def keyword_list_to_text(lst):
    '''process lst into a single long string with words repeated
    according to their weight so that the string can be indexed in
    Solr in a way which makes the term frequency of the keywords
    correspond with the keyword weight'''

    if not lst:
        return ""

    newlst = map(lambda (a,b): (a, int(round(b*1000))), lst)
    
    stringsies = []
    for (a,b) in newlst:
        for i in xrange(b):
            stringsies.append(a)
            
    return "\n".join(stringsies)



class Document:
    '''Class for handling our Solr documents neatly together with Sunburnt.

    Note: .lovekeywords_pylist/.hatekeywords_pylist is the actual list
           structure, yet .lovekeywords_list()/.hatekeywords_list()
           return the list structure in the list format for storing
           into Solr.

           since the fields used in our schema are named:
           lovekeywords_list/hatekeywords_list we can actually just
           add an object of this class to Solr's database elegantly
           using Sunburnt, while excluding the _pylist ones.'''
    
    def __init__(self,
                 id,
                 lovekeywords_list = [],
                 hatekeywords_list = [],
                 since_id = 0,
                 updatecount = 0):
        self.id = id

        # Parse the args if they are strings (otherwise they would normally be lists of tuples etc.etc.)
        self.lovekeywords_pylist = ast.literal_eval(lovekeywords_list) if isinstance(lovekeywords_list, basestring) else lovekeywords_list
        self.hatekeywords_pylist = ast.literal_eval(hatekeywords_list) if isinstance(hatekeywords_list, basestring) else hatekeywords_list
        
        self.since_id = since_id
        self.updatecount = updatecount

    def lovekeywords_list(self):
        # repr gives string representation
        return repr(self.lovekeywords_pylist)

    def hatekeywords_list(self):
        return repr(self.hatekeywords_pylist)

    def lovekeywords_list_scaled(self):
        return repr(scale_keyword_list(self.lovekeywords_pylist))

    def hatekeywords_list_scaled(self):
        return repr(scale_keyword_list(self.hatekeywords_pylist))
    
    def lovekeywords(self):
        return keyword_list_to_text(scale_keyword_list(self.lovekeywords_pylist))

    def hatekeywords(self):
        return keyword_list_to_text(scale_keyword_list(self.hatekeywords_pylist))





