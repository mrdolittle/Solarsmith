#!/usr/bin/python2.7

def weight_total(lst):
    '''Returns the total weight of a list of (keyword, weight) tuples.'''
    return sum(map(lambda x: x[1], lst))

def scale_keyword_list(lst):
    '''Scale list of (keyword, weight) pairs so that the weight will
    be scaled to the interval 0.0 to 1.0 inclusive, that is the
    weights will be relative.'''
    scale = weight_total(lst)
    return map(lambda (a,b): (a, float(b)/scale), lst)

def keyword_list_to_text(lst):
    '''process lst into a single long string with words repeated
    according to their weight so that the string can be indexed in
    Solr in a way which makes the term frequency of the keywords
    correspond with the keyword weight'''

    newlst = map(lambda (a,b): (a, int(round(b*1000))), lst)
    
    stringsies = []
    for (a,b) in newlst:
        for i in xrange(b):
            stringsies.append(a)
            
    return "\n".join(stringsies)

class Document:
    def __init__(self,
                 id,
                 lovekeywords_list = [],
                 hatekeywords_list = [],
                 since_id = 0,
                 updatecount = 0):
        self.id = id
        self.__lovekeywords_list = lovekeywords_list
        self.__hatekeywords_list = hatekeywords_list
        self.since_id = since_id
        self.updatecount = updatecount

    def lovekeywords_list(self):
        # repr gives string representation
        return repr(self.__lovekeywords_list)

    def hatekeywords_list(self):
        return repr(self.__hatekeywords_list)

    def lovekeywords_list_scaled(self):
        return repr(scale_keyword_list(self.__lovekeywords_list))

    def hatekeywords_list_scaled(self):
        return repr(scale_keyword_list(self.__hatekeywords_list))
    
    def lovekeywords(self):
        return keyword_list_to_text(scale_keyword_list(self.__lovekeywords_list))

    def hatekeywords(self):
        return keyword_list_to_text(scale_keyword_list(self.__hatekeywords_list))





