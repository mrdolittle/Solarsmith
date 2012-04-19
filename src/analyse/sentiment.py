"""
@package sentiment
Twitter sentiment analysis.

This code performs sentiment analysis on Tweets.

A custom feature extractor looks for key words and emoticons.  These are fed in
to a naive Bayes CLASSIFIER to assign a label of 'positive', 'negative', or
'neutral'.  Optionally, a principle components transform (PCT) is used to lessen
the influence of covariant features.

"""
import  random
import nltk
import ast
import csv
import tweet_features, tweet_pca
import features
CORPUS1="../analyse/sentiment.csv"
CORPUS2="../analyse/newcorpus3"

def purge_neutral(features_dict):
    global CLASSIFIER
    feature_list=CLASSIFIER.most_informative_features(len(features_dict))
    for feature in feature_list:
        # print dict{[feature])}
        #print word_true_dict(feature[0])
        classification=CLASSIFIER.classify(word_true_dict(feature[0]))
        #print classification
        if classification == 'neutral':
            try:
                features_dict.pop(feature[0])
            except Exception,e:
                None
    for feat in features_dict:
        print feat
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
    
    
    # print features_dict
    #  print sentence
    
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
                #print candidate_feature
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
        #print res
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

def get_words_list(sentence,num_words=2, words_in_feature=3):
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
    # for each num_words
    while num_words <= words_in_feature:
        # add all features with num_words
        start = 0
        end=start + num_words
        while end <= len(words):
            res.append(" ".join(words[start:end]).strip(","))
            start = start + 1
            end = start + num_words
        num_words = num_words + 1
    return res

def readcorpus(filename,tweets):
    with open(filename, 'rb') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
        for row in reader:
            tweets.append([row[4], row[1]])
    

def analyse_sentiment(sentence):
    '''Analyses sentence sentiment. Returns a number of size
    representing sentiment with negative numbers meaning negative
    sentiment.'''
    global CLASSIFIER
    global method
    if method==1:
        featureset=word_true_dict(get_words_list(sentence))
    if method==2:
        featureset=word_true_dict(get_significant_features(sentence,feature_dict))
        
   
    #classification = CLASSIFIER.classify(tweet_features.make_tweet_dict(sentence))
    classification = CLASSIFIER.classify(featureset)
    featureset=None
    if classification == 'negative':
        return -1.0 # byts mot en riktig relevansmetod
    if classification == 'positive':
        return 1.0 # byts mot en riktig relevansmetod
    else:
        return 0.5 # byts mot en riktig relevansmetod


method=1








## read all tweets and labels
with open(CORPUS2, 'rb') as fp:
    tweets = []
    for row in fp:
        tweets.append(ast.literal_eval(row))
if method==1:
    min_length=2
    max_length=3
#Retrieve NEUTRAL SET (appending to tweets list)
if method==2:
    min_length=2
    max_length=3
    readcorpus(CORPUS1,tweets)

    
## treat neutral and irrelevant the same
for t in tweets:
    if t[1] == 'irrelevant':
        t[1] = 'neutral'
        

# training with martins method

v_train = [(word_true_dict(get_words_list(t,min_length,max_length)),s) for (t,s) in tweets]

#training with feature_extraction method
#v_train = [(word_true_dict(features.extract_features(t)),s) for (t,s) in tweets]
tweets=None
# Old tweetlist simplistic tweetfeature
#fvecs = [(tweet_features.make_tweet_dict(t),s) for (t,s) in tweets]



CLASSIFIER = nltk.NaiveBayesClassifier.train(v_train);
v_train=None
feature_dict=None

if method==2:
    feature_dict= {}.fromkeys([t[0] for t in CLASSIFIER.most_informative_features(200000)])
    print len(feature_dict)
    purge_neutral(feature_dict)
    print len(feature_dict)


#CLASSIFIER = nltk.classify.maxent.train_maxent_CLASSIFIER_with_gis(v_train);