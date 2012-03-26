import nltk
from nltk.corpus import wordnet as wn


f = open('englishtweets', 'r')
f2 = open('pospurified', 'w')
f3 = open('negpurified', 'w')
#f4 = open('englishtweets', 'w')

positive =[':-)', ':)',':)', ':D', '=D', '=)', 'C:', ':]',':>', ';)', ';D', ';-)','^^', '^.^', 'xD','XD', '(:', '(-:', '(=', '^.~', '<3', 'c"']
negative =[':-(', ':(', '=(', ":'(", 'D:', 'DX', 'D=', '-.-', "-.-'", ':<', ':[', 'X(', 'x(', '><', '>.<', '>_<', '<.<', '>.>']
#testcommenta

def isenglish(tweet):
    wordlist=tweet.split(" ")
    englishfactor=0
    for word in wordlist: 
        #if it is a english word
        if wn.synsets(word):
            englishfactor=englishfactor+1
            #  a english word
    if ((englishfactor+0.0)/len(wordlist))> 0.4:
        return True
    else:
        return False
            
    
count=0
for line in f:
    line=line.rstrip("\n")
    count=count+1
    words=line.split(" ")
    #print line
    #print words
     
    if count>570 and count<590:
        print line
    if any(x in positive for x in words):
        f2.write(line+'\n')
            
    if any(x in negative for x in words):
        f3.write(line+'\n')
            
    
    if isenglish(line):
        a=2
        #print line
 #       f4.write(line+'\n')
        
        
#TEST
englishsentence= "Who wants to give me a massage??? :)"
words=englishsentence.split()
print words
if any(x in positive for x in words):
         print englishsentence
#if isenglish(englishsentence)==True:
#    print "OMG HAHAHHAHAH SO FUNNY WEEEEEEEEEEEEEEEEEEEEEEEEEEEE"

