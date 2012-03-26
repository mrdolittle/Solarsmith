'''
Keywords

Used to extract keywords from tweets (rather greedy)
Includes methods: extract_keywords

@author: 0tchii, Xantoz
'''

import nltk
from nltk.tag import _POS_TAGGER
import operator
from stopwords import filter_keywords, strip_tweet

def extract_keywords_grammar(text):
    '''Uses chunks matching to identify keywords in a tweet. The code looks much nicer this way :P'''

    sequence = nltk.pos_tag(nltk.word_tokenize(text))
    words = []
    grammar=''' Noun: {<DT>?<JJ>+(<NN>|<NNS>|<VBG>)+}
                ToVerb: {<TO><VB>}
                Name:{<NNP>+}                
            '''
    grammarSingular='''Noun:{(<NN>|<NNS>|<VBG>)}
                        Name: {<NNP>}
                    '''
    chunks = nltk.RegexpParser(grammar)
    chunksSingular = nltk.RegexpParser(grammarSingular)
    
    for t in chunks.parse(sequence).subtrees():
        if t.node == "Noun":
            words.append(reduce(lambda (x,_1),(y,_2): x+" "+y, t))          
        elif t.node == "ToVerb":
            words.append(t[1][0])
        elif t.node == "Name":
            words.append(reduce(lambda (x,_1),(y,_2): x+" "+y, t))  
                
    for s in chunksSingular.parse(sequence).subtrees():
        if s.node == "Noun":
            words.append(s[0][0])
        elif s.node == "Name":
            words.append(s[0][0])
                    
    return words

def get_hashtags(tweet):
    '''Splits tweet on whitespace (this is ok, since hashtags are rarely combined together with
    punctuation in scary ways that other words might be... I think... (TODO: investigate this)) and
    finds hashtags in it.'''
    
    return filter(lambda x: x[0] == '#', tweet.split())

def extract_keywords(tweet):
    '''Extracts hashtags and keywords from a tweet, stores them in a neat little list. Wee'''
    
    return filter_keywords(extract_keywords_grammar(strip_tweet(tweet))) + get_hashtags(tweet)
                    
#Initialize _POS_TAGGER
nltk.data.load(_POS_TAGGER)

if __name__ == '__main__':
    text = "Bear Grylls likes to go spear fishing #fishing"
    print extract_keywords(text)
    print extract(text)
