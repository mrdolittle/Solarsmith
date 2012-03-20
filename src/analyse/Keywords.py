'''
Keywords

Used to extract keywords from tweets (rather greedy)
Includes methods: extract_keywords

@author: 0tchii
'''
import nltk
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
                    
# Very very naughty, fix this:
# Anarchy
# print "Initializing"
# nltk.pos_tag(nltk.word_tokenize("HEJ!"))
# print "Done"
if __name__ == '__main__':
    print extract_keywords("I wanted to go surfing, but I can't because there are too many alligators. This vacation sucks!")
