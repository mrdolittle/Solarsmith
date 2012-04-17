'''
Created on Apr 16, 2012

@author: mbernt
'''

def get_words_list(sentence, words_in_feature):
    '''Used to get all features/words up to the specified
    words_in_feature. 
    Ex. 
    get_words_list("hej pa daj", 2)
    gives 
    ['hej', 'pa', 'daj', 'hej pa', 'pa daj']'''
    # get words in sentence
    words = sentence.lower().split()
    # adjust so that the words_in_feature is less than 
    # the number of words in the sentence
    words_in_feature = min(words_in_feature, len(words))
    res = []
    num_words = 1
    # for each num_words
    while num_words <= words_in_feature:
        # add all features with num_words
        start = 0
        end=start + num_words
        while end <= len(words):
            res.append(" ".join(words[start:end]))
            start = start + 1
            end = start + num_words
        num_words = num_words + 1
    return res

def word_true_tuples(words):
    '''takes a list of words, returns [(word1,True),(word2,True)...]'''
    tuples=[]
    for word in words:
        tuples.append((word,True))
    return tuples
def word_true_dict(words):
    feat={}
    for word in words:
        feat[word]=True
    return feat

#test      
print word_true_dict(get_words_list("hej pa lilla dej", 1))
print get_words_list("hej pa lilla dej", 2)
print get_words_list("hej pa lilla dej", 3)