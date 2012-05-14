"""
@package sentiment
Twitter sentiment analysis.

This code performs sentiment analysis on Tweets.

A custom feature extractor looks for key words and emoticons.  These are fed in
to a naive Bayes CLASSIFIER to assign a label of 'positive', 'negative', or
'neutral'.  Optionally, a principle components transform (PCT) is used to lessen
the influence of covariant features.


"""
import os.path
import pickle
import nltk
import ast
import csv
import features
CORPUS1="../analyse/sentiment.csv"
# CORPUS2="../analyse/newcorpus3"
CORPUS2="../analyse/manual"
# CORPUS2="../analyse/manual.snapshot1"
CORPUS3="../analyse/newcorpus3"
CODE='../analyse/sentiment.py'
TRAINEDBAYES='../analyse/trainedbayes.pickle'

def classifier_contains(trained_classifier, dict_with_features):
    '''Classifier is very stupid, so had to use this workaround.
    It check if the classifier contains any of the feature in
    dict_with_features
    example: 
    classifier_contains(CLASSIFIER,{}.fromkeys(["sibgvosdhgsubvofbhudgu","GdrhdFd"],True))
    gives false, probably'''
    
    listx1=trained_classifier.prob_classify({})
    listx2=listx1.samples()
    
    listy1=trained_classifier.prob_classify(dict_with_features)
    listy2=listy1.samples()
    
    #listx1.prob(listx2[i])
    # compare against default values, if there is a difference then the feature exist, probably
    for booli in map((lambda x, y: listx1.prob(x) == listy1.prob(y)), listx2, listy2):
        if not booli:
            return True
    return False

def get_classification_tuples(prob_classification):
    '''Uses the output from CLASSIFIER.prob_classify as input, and
    gives a list of tuples as output.
    Example output:
    [('positive', 0.7037326500107238), ('neutral', 0.11108935138063251), 
    ('negative', 0.1851779986086436)]'''
    return map((lambda sample: (sample, prob_classification.prob(sample))),  prob_classification.samples())
    
    

def one_features():
    return True
def purge_neutral(features_dict):
    global CLASSIFIER
    feature_list=CLASSIFIER.most_informative_features(len(features_dict))
    for feature in feature_list:
        # print dict{[feature])}
        #print word_true_dict(feature[0])
        classification=CLASSIFIER.classify(word_true_dict(feature[0]))
        print classification
        print feature
        if classification == 'neutral':
            #print features[0]
            try:
                features_dict.pop(feature[0]) 
                print features[0]
            except Exception,e:
                print e
  #  for feat in features_dict:
        #print feat
def get_significant_features(sentence,features_dict, num_words = 2,words_in_feature=3):
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


def classifier_contains_string(dict_with_feature, trained_classifier):
    '''Classifier is very stupid, so had to use this workaround.'''
    # get objects that contain samples and values, and then a list of the names of the samples
    # this is for the default values
    listx1=trained_classifier.prob_classify({})
    listx2=listx1.samples()
    
    # get objects that contain samples and values, and then a list of the names of the samples
    # this is for dict_with_feature
    listy1=trained_classifier.prob_classify(dict_with_feature)
    listy2=listy1.samples()
    
    # compare against default values, if there is a difference then the feature exist, probably
    for booli in map((lambda x, y: listx1.prob(x) == listy1.prob(y)), listx2, listy2):
        if not booli:
            return True
    return False

def get_significant_features_2(sentence, trained_classifier, num_words = 1, words_in_feature=3):
    '''trained_classifier is a trained_classifier naive bayes classifier. This is used to check if the word
    has been classified and at the end to remove the neutral features from the result.'''
    # get words in sentence
    words = get_words(sentence)# sentence.lower().split()
    
    # adjust so that the words_in_feature is less than 
    # the number of words in the sentence
    words_in_feature = min(words_in_feature, len(words))
    res = []
    
    # could place features in lists according to their 
    # startindex so that it's faster to remove sub features
    
    
    
    print sentence
    
    tmp_dict={} 
    
    # for each num_words
    while num_words <= words_in_feature:
        tmpList=[]
        # add all features with num_words
        start = 0
        end=start + num_words
        while end <= len(words):
            # construct feature and strip commas from beginning and end
            candidate_feature=get_feature(words, start, end)#" ".join(words[start:end]).strip(",")
            # only add features
            # TODO: check if this is the correct test to check if the word is in the 
            # trained_classifier classifier
            tmp_dict.clear()
            tmp_dict[candidate_feature]=True
            if classifier_contains_string(tmp_dict,trained_classifier):
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
                            # it's a sub feature so remove it from the result list1
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

    # add non neutral words to the final res list1 (res2)
    res2= []
    list1=[word for (x,y,word) in res]
    for word in list1:
        tmp_dict.clear()
        tmp_dict[candidate_feature]=True
        if trained_classifier.classify(tmp_dict)!="neutral":
            res2.append(word)
    
    # if contain no other than neutral return
    # the list1 with neutral anyway
    if len(res2)>0:        
        return res2
    else:
        return list1


    
        
    

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
def get_feature(words,start,end):
    return " ".join(words[start:end]).strip(",")

def get_words(sentence):
    '''Split into list of words in lower case.'''
    return sentence.lower().split()#re.findall(re.compile(r"[a-z.0-9]+"), sentence.lower())

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
            res.append(get_feature(words,start,end))#" ".join(words[start:end]).strip(","))
            start = start + 1
            end = start + num_words
        num_words = num_words + 1
    return res

def get_words_list_2(sentence, num_words = 1,words_in_feature=3, allowed_features_dict=None):
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
            tmp=get_feature(words,start,end)#res.append(" ".join(words[start:end]).strip(","))
            if allowed_features_dict == None or allowed_features_dict.has_key(tmp):
                res.append(tmp)
            start = start + 1
            end = start + num_words
        num_words = num_words + 1
    return res


def read_csv_corpus(filename,tweets):
    with open(filename, 'rb') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
        for row in reader:
            tweets.append([row[4], row[1]])

def read_corpuses(filenames,tweets):
    for filename in filenames:
        with open(filename, 'rb') as fp:
            for row in fp:
                tweets.append(ast.literal_eval(row))
    
def special_train(tweets, min_length=1, max_length=3, limit=0):
    '''trains a naive bayes and then takes the most informative features to make an allowed_features_dict.
    A new bayes is trained but only with the allowed features,his is then returned. 
    This will make the memory much smaller.
    limit==0 means no limit.'''
    # train with all features with the given min_length and max_length
    training_list = [(word_true_dict(get_words_list(sentence,min_length,max_length)),sentiment) for (sentence,sentiment) in tweets]
    trained_bayes = nltk.NaiveBayesClassifier.train(training_list)
    
    # 0 means no limit so return the result
    if limit == 0:
        return trained_bayes
    
    training_list=None # throw to pacman
    
    # get create a dictionary from the most informative features
    allowed_dict={}.fromkeys([x for (x,y) in trained_bayes.most_informative_features(limit)])
    
    trained_bayes=None # throw to pacman
    
    #print "length of allowed_dict "+ str(len(allowed_dict))
    
    # train with only the most informative features with the given min_length and max_length
    training_list = [(word_true_dict(get_words_list_2(sentence, min_length, max_length, allowed_dict)), sentiment) for (sentence, sentiment) in tweets]
    return nltk.NaiveBayesClassifier.train(training_list)     

def analyse_sentiment(sentence):
    '''Analyses sentence sentiment. Returns a number of size
    representing sentiment with negative numbers meaning negative
    sentiment.'''
    global CLASSIFIER
    global method
    global min_length
    global max_length
    if method==1:
        featureset=word_true_dict(get_words_list(sentence, min_length, max_length))
    if method==2:
        #featureset=word_true_dict(get_significant_features(sentence,feature_dict))
        featureset=word_true_dict(get_significant_features_2(sentence, CLASSIFIER, min_length, max_length))
        
   
    #classification = CLASSIFIER.classify(tweet_features.make_tweet_dict(sentence))
    classification = CLASSIFIER.classify(featureset)
    featureset=None
    if classification == 'negative':
        return -1.0 # byts mot en riktig relevansmetod
    if classification == 'positive':
        return 1.0 # byts mot en riktig relevansmetod
    else:
        return 0.5 # byts mot en riktig relevansmetod







maxtime=0
files=[CORPUS2,CODE,CORPUS1,CORPUS3]
for f in files:
    tmptime = os.path.getctime(f)
    if tmptime > maxtime:
        maxtime=tmptime
bayestime=0

#with open(TRAINEDBAYES) as fp:
try:
    bayestime=os.path.getmtime(TRAINEDBAYES)
except OSError as e:
    print 'Oh dear.'
print ("maxtime is ",maxtime," bayestime is ",bayestime)

##method 1 is reading ONLY the manualtagged corpus and training naivebayes based on that
##method 2 is reading the manualtagged and an other corpus with much more neutral tweets,
## then using get significant_features_2
    
method=2

## DONT RETRAIN NAIVEBAYES IF CURRENT ONE IS UP TO DATE
if maxtime<bayestime and (maxtime!=0 and bayestime!=0):
    with open('../analyse/trainedbayes.pickle','rb') as fp:
        print "LOADING CLASSIFIER FROM FILE"
        CLASSIFIER=pickle.load(fp)
else:    
    print "RETRAINING NAIVEBAYES BECAUSE OF OLD CLASSIFIER FILE"


    ## read all tweets and labels
    tweets = []
    
    # add to list of corpuses
    corpus_list=[]
    corpus_list.append(CORPUS2)
    #corpus_list.append(CORPUS3)
   # if method==2:
        #read_csv_corpus(CORPUS1,tweets) 
        #corpus_list.append(CORPUS1)
        
    # read from the corpuses
    read_corpuses(corpus_list, tweets)
    
    #with open(CORPUS2, 'rb') as fp:
    #    for row in fp:
    #        tweets.append(ast.literal_eval(row))
    #with open(CORPUS3, 'rb') as fp:
    #    for row in fp:
    #        tweets.append(ast.literal_eval(row))
            
    

    print "PRINTING LENGTH OF FULLCORPUS"        
    print len(tweets)
    
        
    ## treat neutral and irrelevant the same
    for t in tweets:
        if t[1] == 'irrelevant':
            t[1] = 'neutral'
    
    # determines the feature size (how many words are in a feature)
    min_length=2
    max_length=3        

    # train with the given tweets and these parameters, limit=0 means no limit
    CLASSIFIER=special_train(tweets,min_length,max_length,0)
    
    v_train=None
    feature_dict=None
    with open('../analyse/trainedbayes.pickle','wb') as f:
        pickle.dump(CLASSIFIER,f)
            
