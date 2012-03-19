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
    words=[]
    
    # Skriv om det har med en ordentlig pattern matcher
    for x in range(0, len(sequence)):
        part = sequence[x]
        # Searching for nouns
        if part[1] in ['NN','NNS','NNP','VBG']:
            words.append(part[0])
            # Searching for adjectives before nouns
            if x>0 and sequence[x-1][1] in ['JJ','NN','NNP','NNS'] and not part[1] in ['NNP']:
                words.append(sequence[x-1][0] +" "+ part[0])
        elif x<len(sequence) and part[1] in ['TO'] and sequence[x+1][1] in ['VB']:
            words.append(sequence[x+1][0])
    words = filter_keywords(words)
    
    return words
                    
# Very very naughty, fix this:
# Anarchy
print "Initializing"
nltk.pos_tag(nltk.word_tokenize("HEJ!"))
print "Done"
print extract_keywords("just got my iphone in the mail, loving it!")