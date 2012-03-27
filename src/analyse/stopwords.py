'''
Stopwords

Defines a list of words that could be seen as keywords but are too vague
Includes methods: filter_keyword

@author: 0tchii, Xantoz
'''

import re

STOPWORDS = set(["something",
                 "nothing",
                 "loving",       # ex: "just got my iphone in the mail, loving it!". This might somehow be appropriate as a keyword though...
                 "hating",        # same as above applies. Strange idea: extract_keywords without filtering then use some extracted keywords for sentiment analysis?
                 "everything",
                 "fun",
                 "lol",
                 "LOL",
                 "ROFL",
                 "ROFLMAO",
                 "ROLFMAO",     # rolling on lava fucking my ass of. The variant ROLF, rolling on laughing floor, is not added since it is a name
                 "rolfmao",
                 "roflmao",
                 "URLYBURLYSMURLYPURLY" # this one is inserted for URL's by word_tokenize, so we filter it (it tends to be tagged as NNP and considered a keyword)
                 ])

def filter_keywords(keywords):
    """Receives the keywords and filters out words from the set 'words'"""
    global STOPWORDS
    
    #return filter(lambda x: x not in words, keywords)
    return [x for x in keywords if x not in STOPWORDS]

# smileys and other words that shouldn't be left intact as to not confuse the keyword-exrctracty shit
# TODO: generate this in some function or something instead, so many combinations!
#       lotsa more smileys and other words that are wierd and stuff.
TWEET_STOPSMILEYS = set([":)", ":(", ":<", ":>", ":-)", ":-(", ":-<", ";-)", ";)", ";(", ";-(",
                         ":3",   # cat
                         ">:3",  # lion
                         "}:3"]) # elk

def split_tweet(text):
    '''Splits tweets neater than regular splitting at whitespace (for
    instance whenever we encounter a hashtag or @-notation we split
    away any punctuation at the end. Doesn't split punctuation from
    words outside of hashtags/@-notation however.'''

    def split_tag(tag):
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

URL_REGEX = re.compile(r'https?:(?:(//)|(\\\\))+[!\w\d:#@%/;$()~_?\+\-=\\\.,&]*', re.I)
def strip_tweet(tweet):
    '''Strips tweet of scary features like hashtags at the start or
    end of a tweet as well as some smileys etc.

    TODO: * test whether this approach to hashtags is not insane etc.
          * More words to transform?
          * DONE keep eventual punctation (or any non-alnum chars really)
            at the end of hashtag when removing it, instead of completely nuking it.
          * DONE? strip at-sign and maybe even split those names at camelCase
          (seems common) (maybe be wholly crazy and get fullname from twitter?)
          * Strip URLS at the very end or so (like hashtags)
          '''
    global TWEET_STOPSMILEYS, URL_REGEX


    def transform(a):
        if a[0:2] == '<3':
            # convert hearts to: love 
            return "love " + a[2:]
        else:
            return a

    urlless_tweet = URL_REGEX.sub("URLYBURLYSMURLYPURLY", tweet)
    words = split_tweet(urlless_tweet)

    # # strip leading hashtags
    # while words != [] and words[0][0] == '#':
    #     del words[0]

    # strip trailing hashtags
    while words != [] and words[-1][0] == '#':
        del words[-1]

    words = map(lambda x: x[1:] if x[0] in ('#','@')  else x, words) # strip the hashes out of hashtags in the middle, as well as stripping @
    words = map(transform, words) 
    words = filter(lambda x: x not in TWEET_STOPSMILEYS, words) # strip the smileys etc. out of the tweet

    return ' '.join(words)
