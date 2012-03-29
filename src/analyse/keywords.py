'''
Keywords

Used to extract keywords from tweets (rather greedy)
Includes methods: extract_keywords

@author: 0tchii, Xantoz
'''

import nltk
from nltk.tag import _POS_TAGGER
from stopwords import filter_keywords, strip_tweet

def extract_keywords_grammar(text):
    '''Uses chunks matching to identify keywords in a tweet. The code looks much nicer this way :P'''
    
    sequence = nltk.pos_tag(nltk.word_tokenize(text))
    words = []
    grammar=''' Noun: {<DT>?<JJ>+(<NN>|<NNS>|<VBG>)+}
                ToVerb: {<TO><VB>}
                Name:{<NNP><NNP>+}                
            '''
    grammarSingular='''Noun: {(<NN>|<NNS>|<VBG>)}
                        Name: {<NNP>}
                    '''
    chunks = nltk.RegexpParser(grammar)
    chunksSingular = nltk.RegexpParser(grammarSingular)
    
    for t in chunks.parse(sequence).subtrees():
        if t.node == "Noun":
            if len(t[0][0])>1:
                keys = reduce(lambda x,y: x + " " + y, map(lambda (x,_1): x, t)).lower()            
                words.append(keys)         
        elif t.node == "ToVerb":
            if len(t[0][0])>1:
                words.append(t[1][0].lower())
        elif t.node == "Name":
            if len(t[0][0])>1:
                words.append(reduce(lambda x,y: x + " " + y, map(lambda (x,_1): x, t)).lower()) 
                
    for s in chunksSingular.parse(sequence).subtrees():
        if s.node == "Noun":
            if len(t[0][0])>1:
                words.append(s[0][0].lower())
        elif s.node == "Name":
            if len(t[0][0])>1:
                words.append(s[0][0].lower())
                    
    return words

# def extract(text,words):
#     hashtagreturn = strip_hashtags(text,words)
#     return extract_keywords_grammar(hashtagreturn[0], hashtagreturn[1])

def get_hashtags(tweet):
    '''Splits tweet on whitespace (this is ok, since hashtags are rarely combined together with
    punctuation in scary ways that other words might be... I think... (TODO: investigate this)) and
    finds hashtags in it.'''
    
    return filter(lambda x: x[0] == '#', tweet.split())

def extract_keywords(sentence):
    '''Extracts hashtags and keywords from a tweet, stores them in a neat little list of tuples of
    keyword and a confidence factor of some sort (currently hard-coded to 1.0. But might change in
    future, or might not and just be really stupid). '''
    
    return map(lambda a: (a,1.0), filter_keywords(extract_keywords_grammar(strip_tweet(sentence))) + get_hashtags(sentence))                
#Initialize _POS_TAGGER
nltk.data.load(_POS_TAGGER)

if __name__ == '__main__':
    text = "Let's be honest, folks. Google Chrome is amazingly superior to IE"
    print extract_keywords(text)
    
