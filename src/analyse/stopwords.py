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
                 "hating"        # same as above applies. Strange idea: extract_keywords without filtering then use some extracted keywords for sentiment analysis?
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
                         
 
                          

URL_REGEX = re.compile(r'https?:(?:(//)|(\\\\))+[!\w\d:#@%/;$()~_?\+\-=\\\.,&]*', re.I)
def strip_tweet(tweet):
    '''Strips tweet of scary features like hashtags at the start or
    end of a tweet as well as some smileys etc.

    TODO: test whether this approach to hashtags is not insane etc.
          More words to transform?'''
    global TWEET_STOPSMILEYS, URL_REGEX

    urlless_tweet = URL_REGEX.sub("", tweet)
    words = urlless_tweet.split()

    # strip leading hashtags
    while words != [] and words[0][0] == '#':
        del words[0]

    # strip trailing hashtags
    while words != [] and words[-1][0] == '#':
        del words[-1]

    words = map(lambda x: x[1:] if x[0] == '#' else x, words) # strip the hashes out of hashtags in the middle
    words = map(lambda x: "love" if x == "<3" else x, words) # convert hearts to: love (is this really really stupid? Or perhaps
                                                             # should be the focus of another function than this one) (kinda
                                                             # stupid since "sdf adf <3." the last word (when splitting on
                                                             # whitespace) will be "<3.". Maybe just strip these things always?
    words = filter(lambda x: x not in TWEET_STOPSMILEYS, words) # strip the smileys etc. out of the tweet

    return ' '.join(words)
