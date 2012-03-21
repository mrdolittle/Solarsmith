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
    sequence=reduce(operator.add, map(nltk.pos_tag, map(nltk.word_tokenize, nltk.sent_tokenize(string))))
    length=len(sequence)
    
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

def extract_keywords_chunks(text):
    sequence=reduce(operator.add, map(nltk.pos_tag, map(nltk.word_tokenize, nltk.sent_tokenize(text))))
    grammar=''' Noun: {<DT>?<JJ>*(<NN>|<NNS>|<VBG>)+}
                ToVerb: {<TO><VB>}
                Name:{<NNP>+}                
            '''
    words=[]
    chunks = nltk.RegexpParser(grammar)
    for t in chunks.parse(sequence).subtrees():
        if t.node=="Noun":
            print t.flatten()           
        elif t.node=="ToVerb":
            for x in t:
                if x[1]!="TO":
                    words.append(x[0])
        elif t.node=="Name":
            for x in t:
                words.append(x[0])
                
            
    return chunks.parse(sequence)
                    
#Initialize _POS_TAGGER
nltk.data.load(_POS_TAGGER)

if __name__ == '__main__':
    text = "Bear Grylls likes to go spear fishing"
    print extract_keywords(text)
    print extract_keywords_chunks(text)
