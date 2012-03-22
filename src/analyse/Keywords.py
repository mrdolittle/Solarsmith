'''
Keywords

Used to extract keywords from tweets (rather greedy)
Includes methods: extract_keywords

@author: 0tchii
'''

import nltk
from nltk.tag import _POS_TAGGER
import operator
from Stopwords import filter_keywords

def extract_keywords(string):
    '''Receives a string and returns a list of extracts keywords'''
    
    sequence = reduce(operator.add, map(nltk.pos_tag, map(nltk.word_tokenize, nltk.sent_tokenize(string))))
    length = len(sequence)
    
    def doStuff(x, words):
        '''Recursive help method to parse for keywords and keyword sequences'''
        (thisWord, this) = sequence[x]
        (nextWord, nxt) = sequence[x+1]
        
        #Checks for adjectives followed by nouns or double nouns 
        if this in ['JJ','NN','NNP','NNS'] and nxt in ['NN','NNS','NNP','VBG']:
            #Avoids adjectives followed by names
            if not(this=='JJ' and nxt=='NNP'):
                words.append(thisWord + " "+nextWord)
                
        #Checks for verbs after 'to'
        if this in ['TO'] and nxt in ['VB']:
            words.append(nextWord)
            
        #Checks for simple nouns
        if this in ['NN','NNS','NNP','VBG']:
            words.append(thisWord)
            
        #Fix for last word
        if x==(length-2) and nxt in ['NN','NNS','NNP','VBG']:
            words.append(nextWord)
                    
        #Keep recursing or return            
        if x+1<(length-1):
            return doStuff(x+1, words)
        else:
            return filter_keywords(words)

    return doStuff(0, [])

def strip_hashtags(text, words):
    '''Searches for hashtags and adds the tag to the list of keywords.
    Removes these from the sequence so that it can later be used by extract_keywords_grammar'''
    
    sequence = reduce(operator.add, map(nltk.pos_tag, map(nltk.word_tokenize, nltk.sent_tokenize(text))))
    length = len(sequence)
    x = 0
    while (x < length):
        elem = sequence[x]
        if elem[0] == '#':
            del sequence[x]
            length = length-1     
            if x < length:
                words.append(sequence[x][0])
                del sequence[x]
                length = length - 1
                x = x - 1
            x = x - 1
        x = x + 1
    print words
    return (words,sequence)          
        
#Using grammar
def extract_keywords_grammar(words, sequence):
    '''Uses chunks matching to identify keywords in a tweet. The code looks much nicer this way :P'''
    
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

def extract(text,words):
    hashtagreturn = strip_hashtags(text,words)
    return extract_keywords_grammar(hashtagreturn[0], hashtagreturn[1])
                    
#Initialize _POS_TAGGER
nltk.data.load(_POS_TAGGER)

if __name__ == '__main__':
    text = "Bear Grylls likes to go spear fishing #fishing"
    print extract_keywords(text)
    print extract(text, [])
