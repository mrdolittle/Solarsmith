'''This file contains all the functions responsible for mashing the
various analysis results into the format that the result that the rest
of the project is expecting (two keyword lists with tuples of keyword
and weight).

This is what implements the actual analyse function that we export in __init__.py 
'''

from keywords import extract_keywords
from sentiment import analyse_sentiment

def analyse_sentence(sentence):
    '''Takes a tweet and performs sentimentanalysis on the given tweet, 
    then gives the weight that returns from the sentiment analysis'''
    
    sentiment=analyse_sentiment(sentence)
    keywordtuples = extract_keywords(sentence)
    return [(keyword,sentiment*weight) for (keyword,weight) in keywordtuples]

def analyse_sentences(sentences):
    '''Does analysis of all sentences and returns a compilation of all
    results in the form of two lists'''

def analyse(tweets):
    '''Do the whole analysis shebang and return the results as one lovekeyword list and one hatekeyword list.

    Ex:
    (love, hate) = analyse(tweets)
    print love => [("cat", 34), ("fishing", 22), ("bear grylls", 33)]
    print hate => [("dog", 123), ("bear hunting", 44)]'''
    
    sentences = reduce(lambda x,y: x.append(y), map(nltk.sent_tokenize, tweetlist))
    return analyse_sentences(sentences)
