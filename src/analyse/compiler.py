'''This file contains all the functions responsible for mashing the various analysis results into
the format that the result that the rest of the project is expecting (two keyword lists with tuples
of keyword and weight).

This is what implements the actual analyse function that we export in __init__.py
'''

import nltk
from keywords import extract_keywords
from sentiment import analyse_sentiment
from common import *

#### TODO:
# Do some sort of stemming somewhere around here (at least stem
#       away plurals!) or alternatively at the end of
#       extract_keywords. Also see non_aggressive_stemmer in
#       extract_keywords which aims to be the same thing but isn't
#       maybe we should focus on that
# Some sort of database of keyword implications. like
# pottermore -> harry potter, justin beaver -> justin bieber.
# Probably weighted a percentage (0.8 or so) of the original keywords' weight

def analyse_sentence(sentence):
    '''Takes a tweet and performs sentiment analysis on the given
    tweet, then gives the weight that was returned from the sentiment
    analysis

    TODO: Is this function neccesary? HALF-DEPRECATED'''
    
    sentiment = analyse_sentiment(sentence)
    keywordtuples = extract_keywords(sentence)
    return [(keyword,sentiment*weight) for (keyword,weight) in keywordtuples]

def analyse_sentences_var_1(sentences):
    '''Does analysis of all sentences and returns a compilation of all results in the form of two
    lists in the magical and fantastical format we all know and love.

    ...'''

    hatekeywords = {}
    lovekeywords = {}
    for sentence in sentences:
        sentiment = analyse_sentiment(sentence)
        for (keyword, weight) in extract_keywords(sentence):
            a = lovekeywords if sentiment > 0.0 else hatekeywords  # choose where to put keyword
            a[keyword] = a.get(keyword, 0.0) + weight*abs(sentiment) # only positive weights in end result

    return (lovekeywords.items(), hatekeywords.items())

def analyse_sentences_var_2_helper(sentences):
    '''Does analysis of all sentences and returns a compilation of all results in the form of one
    list of tuples where the weight might be negative or positive depending on the overall sentiment
    around the keyword.'''

    keywords = {}
    for sentence in sentences: 
        for (keyword, weight) in analyse_sentence(sentence):
            keywords[keyword] = keywords.get(keyword, 0.0) + weight

    return keywords.items()

def splittify(keywords):
    '''Takes a list of keywords with positive/negative weights and
    returns two lists on with all the keywords that had positive
    weigths and one with all the negative (or 0) weights.'''
    # Homework for the ones interested in the perversions of lists and functional
    # programming. (This just might be the Haskell way to do it..., or Lisp for that matter).

    return tuple(map(lambda x: list(filter(lambda a: a != None, x)), apply(zip, [((k,w), None) if w > 0.0 else (None, (k,-w)) for (k,w) in keywords])))

def analyse_sentences_var_2(sentences):
    '''This doesn't count love and hate separately but tries to, for each keyword, get only one
    value which is the total amount of love minus the total amount of hate (typing this felt kind of
    wierd...).'''
    
    a = splittify(analyse_sentences_var_2_helper(sentences))
    return ([], []) if not a else a

def analyse(tweets):
    '''Do the whole analysis shebang and return the results as one lovekeyword list and one
    hatekeyword list.
    Ex:
    (love, hate) = analyse(tweets)
    print love => [("cat", 34), ("fishing", 22), ("bear grylls", 33)]
    print hate => [("dog", 123), ("bear hunting", 44)]'''
    # print tweets
    # print map(nltk.sent_tokenize,tweets)
    # print reduce(lambda x,y: x+y,[['tweetlist'], ['lol dont like apples'], ['like reading books']])
    #reduce(lambda x,y: x+y,map(nltk.sent_tokenize, tweets))

    # split the list of tweets to a list of sentences and send it to analyse_sentences
    return analyse_sentences_var_2(reduce(lambda x,y: x+y,
                                          map(nltk.sent_tokenize, filter(isenglish, tweets)),
                                          []))

if __name__ == "__main__":
    print analyse(["Star Wars is the movie of the century","Bear Grylls is being tortured by us more and more"])
    
