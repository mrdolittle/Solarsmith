'''
Keywords

Used to extract keywords from tweets (rather greedy)
Includes methods: extract_keywords

@author: 0tchii, Xantoz
'''

import nltk
from nltk.tag import _POS_TAGGER
from stopwords import filter_keywords, strip_tweet
from common import *
import operator

def extract_keywords_grammar(text):
    '''Uses chunks matching to identify keywords in a tweet. The code looks much nicer this way :P'''
    
    sequence = nltk.pos_tag(nltk.word_tokenize(text))
    words = []
    grammar=''' Noun: {<DT>?<JJ>+(<NN>|<NNS>|<VBG>)+}
                ToVerb: {<TO><VB>}
                Name:{<NNP>*}                
            '''
    grammarSingular='''Noun: {(<NN>|<NNS>|<VBG>)}
                        Name: {<NNP>}
                    '''
    chunks = nltk.RegexpParser(grammar)
    chunksSingular = nltk.RegexpParser(grammarSingular)
    
    for t in chunks.parse(sequence).subtrees():
        if t.node == "Noun":
            keys = reduce(lambda x,y: x + " " + y, map(lambda (x,_1): x, t))            
            words.append((keys,1.0))         
        elif t.node == "ToVerb":
            words.append((t[1][0],1.0))
        elif t.node == "Name":
            if len(t)>1:
                words.append((reduce(lambda x,y: x + " " + y if len(y)>2 else x, map(lambda (x,_1): x, t)), 1.0))
                for x in t:
                    words.append((x[0],0.5))   
            else:
                words.append((t[0][0],1.0))
                
    for s in chunksSingular.parse(sequence).subtrees():
        if s.node == "Noun":
            words.append((s[0][0].lower(),1.0))                    
    return words

# def extract(text,words):
#     hashtagreturn = strip_hashtags(text,words)
#     return extract_keywords_grammar(hashtagreturn[0], hashtagreturn[1])

def get_hashtags(tweet):
    '''Splits tweet and finds hashtags in it.'''
    
    return filter(lambda x: x[0:1] == '#', split_tweet(tweet))

def get_names(tweet):
    '''Splits tweet and finds @username usage in it. Returns names
    without leading @'''
    
    return [x[1:] for x in split_tweet(tweet) if x[0:1] == '@']



def non_aggresive_stemmer(word):
    '''Should stem some simple non-aggresive stuff. Like plurals and genitives.

    TODO: implement me'''

    return word
    

def explicit_keywords(words):
    '''Recognizes certain hard-coded keywords that extract_keywords
    just might miss. If extract_keywords will find them this gives
    them a higher priority so this can also be seen as a sort of boost
    to certain keywords.'''

    # TODO: more?
    keywords = set(['google', 'microsoft', 'apple', 'adobe', 'flash', 'internet', 'tv'])
    return map(lambda x: (x, 1.1), filter(lambda x: x.lower() in keywords, words))
    

def extract_keywords(sentence):
    '''Extracts hashtags and keywords from a tweet, stores them in a
    neat little list of tuples of keyword and a confidence factor of
    some sort (currently hard-coded to 1.0. But might change in
    future, or might not and just be really stupid).'''
    
    def concat(*a):
        return reduce(operator.add, a, [])

    stripped = strip_tweet(sentence)

    names    = set(get_names(sentence)) # made into sets to speed up the filtering below
    hashtags = get_hashtags(sentence)
                    
    return concat(filter(lambda (a,_1): a not in names 
                         map(lambda (a,b): (a.lower(), b),
                             concat(explicit_keywords(map(non_aggresive_stemmer, nltk.word_tokenize(stripped))),
                                    map(non_aggresive_stemmer, filter_keywords(extract_keywords_grammar(stripped),
                                                                               key = lambda a: a[0]))))),
                  map(lambda x: (x.lower(), 5.0), hashtags),
                  map(lambda x: (x.lower(), 1.6), names))

#Initialize _POS_TAGGER
nltk.data.load(_POS_TAGGER)

if __name__ == '__main__':
    text = "Star is a nice guy"
    print extract_keywords_grammar(text)
    
