'''
Stopwords

Defines a list of words that could be seen as keywords but are too vague
Includes methods: filter_keyword

@author: 0tchii
'''
stopwords = set(["something",
                 "nothing",
                 "loving",       # ex: "just got my iphone in the mail, loving it!". This might somehow be appropriate as a keyword though...
                 "hating"        # same as above applies. Strange idea: extract_keywords without filtering then use some extracted keywords for sentiment analysis?
                 ])

def filter_keywords(keywords):
    """Receives the keywords and filters out words from the set 'words'"""
    global stopwords
    #return filter(lambda x: x not in words, keywords)
    return [x for x in keywords if x not in stopwords]
