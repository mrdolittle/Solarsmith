'''
Keywords

Used to extract keywords from tweets (rather greedy)
Includes methods: extract_keywords

@author: 0tchii
'''
import nltk
from Stopwords import filter_keywords

def extract_keywords(string):
    '''Receives a string and returns a list of extracts keywords'''
    
    sequence=nltk.pos_tag(nltk.word_tokenize(string))
    
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
            
        if x+1<(len(sequence)-1):
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
    print extract_keywords("just got my iphone in the mail, loving it!")
