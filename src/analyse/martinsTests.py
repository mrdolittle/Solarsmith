'''
Created on Apr 16, 2012

This file is for experimental code!
Copy paste the code to where it can be used.

ideas
1. train on all words then use this to construct a important features dictionary. 
Then replace non-features with "." and train an additional bayesian thing on these sentences 
(could alternatively replace with POS-tags instead of ".", if the POS-tagging is good enough).
get_words_list2 # not tested enough

2. if larger feature is a real feature and contains real smaller feature then only use the larger when classifying.
get_significant_features # not tested enough

3. combine 1 and 2, and use very large features in 2 (can still use relatively small features in 1). 
The combination of these two give the effect that it tries to find as large features as possible 
but falls back to smaller features if no larger features are found. 
My hypothesis is that larger features are more likely to be correct.

4. normalize the points of the features so that a feature can't dominate the sentiment as easily.

5. give more points to features consisting of multiple words because they are more likely to be correct.

6. Use the ratio between positive, neutral and negative as a very strong factor when calculating points.
Neutral is also important.

7. Train on neutral sentences also, but remove neutral features from naive bayes after training, 
so that neutral features (like "ice-cream") are removed.

Special cases
1. If a not or similar negating statement is before a postive feature, maybe the whole feature is negative?


2. maybe use bayesian thing to find negating statements

@author: mbernt
'''
import re




def get_words_list(sentence, num_words = 1,words_in_feature=3):
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
    # for each num_words
    while num_words <= words_in_feature:
        # add all features with num_words
        start = 0
        end=start + num_words
        while end <= len(words):
            # construct feature and strip commas from beginning and end
            res.append(" ".join(words[start:end]).strip(","))
            start = start + 1
            end = start + num_words
        num_words = num_words + 1
    return res

def get_significant_features(sentence,features_dict, num_words = 1,words_in_feature=3):
    '''Can be used when classifying, so that "don't like" isn't affected by like.
    
    Returns the features but without the sub features like the like in "don't like".
    
    This method can be rewritten to use some other way to check if a candidate feature is a 
    important feature.'''
    # get words in sentence
    words = get_words(sentence)# sentence.lower().split()
    
    # adjust so that the words_in_feature is less than 
    # the number of words in the sentence
    words_in_feature = min(words_in_feature, len(words))
    res = []
    
    # could place features in lists according to their 
    # startindex so that it's faster to remove sub features
    
    
    print features_dict
    print sentence
    
    # for each num_words
    while num_words <= words_in_feature:
        tmpList=[]
        # add all features with num_words
        start = 0
        end=start + num_words
        while end <= len(words):
            # construct feature and strip commas from beginning and end
            candidate_feature=" ".join(words[start:end]).strip(",")
            # only add features
            if features_dict.has_key(candidate_feature):
                print candidate_feature
                # add the word and the index to tmpList
                tmpList.append((start, end, candidate_feature))
            start = start + 1
            end = start + num_words
        
         
        # remove if sub-feature
        # warning! bad time complexity! O(len(res)*len(tmpList))
        keepList=[]
        if num_words>1:
            for (i,j,word) in res:
                add=True
                for (i2,j2,word2) in tmpList:
                    # must be in the same place to be a sub feature
                    if i2<=i and j<=j2:
                        # must be in the larger feature to be a sub feature
                        if word2.find(word)!=-1:
                            # it's a sub feature so remove it from the result list
                            add=False
                            #res.remove((i,j,word))
                # is not a sub feature so keep it
                if add:
                    keepList.append((i,j,word))
        res=keepList
                            
        res=res+tmpList
        print res
        # next number of words
        num_words = num_words + 1
        
    #return only the words without the start indexes
    return [word for (x,y,word) in res]
    
        
    

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
    '''Split into list of words in lower case.'''
    return sentence.lower().split()#re.findall(re.compile(r"[a-z.0-9]+"), sentence.lower())

def replace_nonfeatures(sentence, first_features_dict, num_words, words_in_feature,replace_with="."):
    '''Takes a sentence and replaces all non_features with the replace string ".".
    non_feastures is those "features" that aren't in the first_features_dict.
    The first_features_dict is a dictionairy constructed from the features
    found on a previous run of the bayesian thing, but that used all words as features.
    
    Can later be used if replacing non_features with "." and training on that data 
    '''
    print first_features_dict
    print sentence
    # get words in sentence
    words = get_words(sentence)#sentence.lower().split()
    #print words
    
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

def get_words_list2(sentence, 
                  first_features_dict, num_words_in_dict = 1, words_in_feature_int_dict=3,
                  num_words= 1, words_in_feature=20):   
    '''Can only be used if you already has a list of features, in the form of a dictionary.
    This list can be made in the usual way (train with all words considered as features and then
    get the words with enough points).
    
    This dictionary is used to replace non-features with "." and uses get_words_list to return a list
    of possible features. 
    
    ex 
    get_words_list2("I really like the wonderful mac-air",{}.fromkeys(["really","really like","wonderful"]))
    gives
    ['really', 'like', 'wonderful', '. really', 'really like', 'like .', '. wonderful', 'wonderful .',
    '. really like', 'really like .', 'like . wonderful', '. wonderful .', '. really like .',
     'really like . wonderful', 'like . wonderful .', '. really like . wonderful', 'really like . wonderful .',
      '. really like . wonderful .']
    
    This method will make the training data more general, hopefully.
    
    Remember you have to use this method also when classifying to get the correct features.
    '''
    #print get_words_list(sentence,num_words,words_in_feature)
    #print sentence
    sentence=replace_nonfeatures(sentence, first_features_dict, num_words_in_dict, words_in_feature_int_dict)
    print sentence
    #print sentence
    listy=get_words_list(sentence, num_words, words_in_feature)
    res=[]
    for feature in listy:
        # check if the 
        #print feature
        if len(feature.replace(" ","").replace(".","")):
            res.append(feature)
    return res

#test      
#print word_true_dict(get_words_list("hej pa lilla dej", 1))
#print get_words_list("hej pa lilla dej", 2)
#print get_words_list("hej pa lilla dej", 3)

dicti={}.fromkeys(["really","like","really like","wonderful"])

#print replace_nonfeatures("I really like the wonderful mac-air",dicti,1,3)
#print get_words_list2("I really like the wonderful mac-air",{}.fromkeys(["really","like","really like","wonderful"]))
print get_significant_features("I really like the wonderful mac-air",{}.fromkeys(["really","like","really like","wonderful"]))

