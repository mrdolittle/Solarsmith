import nltk
from nltk.corpus import wordnet
from features import extract_features

corpus = open('corpus', 'r')
sentimentcorpus = open('sentimentcorpus', 'w')
features = open('features', 'w')
englishCorpus = open('englishtweets', 'w')

positive =[':-)', ':)',':)', ':D', '=D', '=)', 'C:', ':]',':>', ';)', ';D', ';-)','^^', '^.^', 'xD','XD', '(:', '(-:', '(=', '^.~', '<3', 'c"']
negative =[':-(', ':(', '=(', ":'(", 'D:', 'DX', 'D=', '-.-', "-.-'", ':<', ':[', 'X(', 'x(', '><', '>.<', '>_<', '<.<', '>.>']
#testcommenta

def isenglish(tweet):
    wordlist=tweet.split(" ")
    englishfactor=0
    for word in wordlist: 
        if wordnet.synsets(word):
            englishfactor=englishfactor+1
            #  a english word
    if ((englishfactor+0.0)/len(wordlist))> 0.4:
        return True
    else:
        return False
            

for line in corpus:
    featurelist=[]
    line=line.rstrip("\n")
    sentences=nltk.sent_tokenize(line)
    
    for sentence in sentences:
        words=sentence.split()
        featurelist.append(extract_features(sentence))
        features.write(featurelist+'\n')
        
        if isenglish(sentence):
            englishCorpus.write(sentence+'\n')
            if any(x in negative for x in words):
                sentimentcorpus.write('"'+sentence+'"'+','+'"'+ "negative" +"'"+'\n')
                
            if any(x in positive for x in words):
                sentimentcorpus.write('"'+sentence+'"'+','+'"'+ "positive" +"'"+'\n')
            
        
