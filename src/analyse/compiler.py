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
    then gives the weight that was returned from the sentiment analysis

    TODO: Is this function neccesary? HALF-DEPRECATED'''
    
    sentiment = analyse_sentiment(sentence)
    keywordtuples = extract_keywords(sentence)
    return [(keyword,sentiment*weight) for (keyword,weight) in keywordtuples]

def analyse_sentences_var_1(sentences):
    '''Does analysis of all sentences and returns a compilation of all
    results in the form of two lists in the magical and fantastical
    format we all know and love.

    ...'''

    def foo(keywords_dict):
        lovekeywords[keyword] = lovekeywords.get(keyword, 0.0)

    hatekeywords = {}
    lovekeywords = {}
    for sentence in sentences:
        sentiment = analyse_sentiment(sentence)
        for (keyword, weight) = extract_keywords(sentence):
            a = lovekeywords if sentiment > 0.0 else hatekeywords
            a[keyword] = a.get(keyword, 0.0)*weight*abs(sentiment)

    return (list(lovekeywords), list(hatekeywords))

def analyse(tweets):
    '''Do the whole analysis shebang and return the results as one lovekeyword list and one hatekeyword list.

    Ex:
    (love, hate) = analyse(tweets)
    print love => [("cat", 34), ("fishing", 22), ("bear grylls", 33)]
    print hate => [("dog", 123), ("bear hunting", 44)]'''

    # split the list of tweets to a list of sentences and send it to analyse_sentences
    return analyse_sentences_var_1(reduce(lambda x,y: x.append(y), map(nltk.sent_tokenize, tweetlist)))
