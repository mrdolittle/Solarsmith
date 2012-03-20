'''
Stopwords

Defines a list of words that could be seen as keywords but are too vague
Includes methods: filter_keyword

@author: 0tchii
'''
stopwords = set(["something",
             "nothing"])

def filter_keywords(keywords):
    """Receives the keywords and filters out words from the set 'words'"""
    global stopwords
    #return filter(lambda x: x not in words, keywords)
    return [x for x in keywords if x not in stopwords]
