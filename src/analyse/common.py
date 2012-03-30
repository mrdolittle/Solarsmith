'''
Some routines used throughout the analyse modules
'''

from nltk.corpus import wordnet
import re

def nop(a):
    '''The identity function'''
    
    return a


def split_tweet(text):
    '''Splits tweets neater than regular splitting at whitespace (for
    instance whenever we encounter a hashtag or @-notation we split
    away any punctuation at the end. Doesn't split punctuation from
    words outside of hashtags/@-notation however.'''

    def split_tag(tag):
        if len(tag) < 2:        # avoid blowing up 
            return [" "]
        [(a, b)] = re.findall(r'([#@]\w+)(.*)', tag) # this will blow up if more than one match (but it won't due to the regex...)
        return [a] if b == '' else [a,b]

    wordsplit = text.split()
    result = []
    for i in wordsplit:
        if i[0] in ('#','@'):
            result = result + split_tag(i)
        else:
            result.append(i)
    return result


def isenglish(tweet):
    '''Ascertains the englishness of the tweet. I say!'''
    
    wordlist = tweet.split()
    
    if len(wordlist) == 0:
        return False
    
    englishfactor = 0
    for word in wordlist: 
        if wordnet.synsets(word):
            englishfactor = englishfactor + 1
            #  a english word
    return True if (englishfactor + 0.0)/len(wordlist) > 0.4 else False

