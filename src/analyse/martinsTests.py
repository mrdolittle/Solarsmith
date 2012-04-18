'''
Created on Apr 16, 2012

@author: mbernt
'''
import re

def get_words_list(sentence, words_in_feature):
    '''Used to get all features/words up to the specified
    words_in_feature. 
    Ex. 
    get_words_list("hej pa daj", 2)
    gives 
    ['hej', 'pa', 'daj', 'hej pa', 'pa daj']'''
    # get words in sentence
    words = get_words(sentence)# sentence.lower().split()
    
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

def get_words(sentence):
    return re.findall(re.compile(r"[a-z.]+"), sentence.lower())

def replace_nonfeatures(sentence, first_features_dict, num_words, words_in_feature,replace_with="."):
    '''Takes a sentence and replaces all non_features with the replace string ".".
    non_feastures is those "features" that aren't in the first_features_dict.
    The first_features_dict is a dictionairy constructed from the feastures
    found on a previous run of the bayesian thing, but that used all words as features.
    
    Can later be used if replacing non_features with "." and training on that data 
    '''
    # get words in sentence
    words = get_words(sentence)#sentence.lower().split()
    
    # adjust so that the words_in_feature is less than 
    # the number of words in the sentence
    words_in_feature = min(words_in_feature, len(words))
    
    # create boolean array
    keeping = [False for ignore in words]
    #keeping = map((lambda x: False)  ,words)


    # for each num_words
    while num_words <= words_in_feature:
        # check if feature and set keeping to true if feature
        start = 0
        end=start + num_words
        while end <= len(words):
            tmp=" ".join(words[start:end])
            #print tmp
            if first_features_dict.has_key(tmp):
                #print tmp
                i=start
                while i<end:
                    keeping[i]=True
                    i=i+1
            start = start + 1
            end = start + num_words
        num_words = num_words + 1
    
    # replace with '.' those that are keeping==false
    return " ".join(map((lambda word, keep: word if keep else replace_with)   ,words,keeping))   
        

#test      
#print word_true_dict(get_words_list("hej pa lilla dej", 1))
#print get_words_list("hej pa lilla dej", 2)
#print get_words_list("hej pa lilla dej", 3)

features=["hej","lilla dej"]
dicti={}.fromkeys(features,None)
print replace_nonfeatures("hej pa, lilla dej",dicti,1,3)
#re.split(r'\W')
#print filter(lambda x: not re., re.split(re.compile(r"([^a-z])+"), "hej.pa.lilla."))
#print re.findall(re.compile(r"[a-z.]+"), "hej ,g. pa . lilla .")
