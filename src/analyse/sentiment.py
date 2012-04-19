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
CORPUS1="../analyse/sentiment.csv"
CORPUS2="../analyse/newcorpus3"


    
def word_true_dict(words):
    feat={}
    for word in words:
        feat[word]=True
    return feat

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
            res.append(" ".join(words[start:end]))
            start = start + 1
            end = start + num_words
        num_words = num_words + 1
    return res

def analyse_sentiment(sentence):
    '''Analyses sentence sentiment. Returns a number of size
    representing sentiment with negative numbers meaning negative
    sentiment.'''
    global CLASSIFIER
    featureset=word_true_dict(get_words_list(sentence))
    #probclass=CLASSIFIER.prob_classify(featureset)
    #listig =probclass.samples()
    #print probclass.max()
    #for sample in listig:
    #    print str(sample)+" "+str(probclass.prob(sample))
    #classification = CLASSIFIER.classify(tweet_features.make_tweet_dict(sentence))
    classification = CLASSIFIER.classify(featureset)
    if classification == 'negative':
        return -1.0 # byts mot en riktig relevansmetod
    if classification == 'positive':
        return 1.0 # byts mot en riktig relevansmetod
    else:
        return 0.5 # byts mot en riktig relevansmetod
    
## read all tweets and labels
with open(CORPUS2, 'rb') as fp:
    
    #reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
    tweets = []
    for row in fp:
        #print row
        tweets.append(ast.literal_eval(row))
#      tweets.append([row[4], row[1]])
#with open(CORPUS1, 'rb') as fp:
#    reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
#    for row in reader:
#        tweets.append([row[4], row[1]])

    
## treat neutral and irrelevant the same
for t in tweets:
    if t[1] == 'irrelevant':
        t[1] = 'neutral'
        
## split in to training and test sets

random.shuffle(tweets);
#word_true_dict(get_words_list("hej pa lilla dej", 1))
fvecs = [(word_true_dict(get_words_list(t)),s) for (t,s) in tweets]
#fvecs = [(tweet_features.make_tweet_dict(t),s) for (t,s) in tweets]
v_train = fvecs
#v_test  = fvecs[2000:]
#print fvecs[1]


#dump tweets which our feature selector found nothing
#for i in range(0,len(tweets)):
    #if tweet_features.is_zero_dict( fvecs[i][0] ):
        #print tweets[i][1] + ': ' + tweets[i][0]




## train CLASSIFIER

CLASSIFIER = nltk.NaiveBayesClassifier.train(v_train);
#cpdist = CLASSIFIER._feature_probdist 
#for (fname, fval) in CLASSIFIER.most_informative_features(100):
#        def labelprob(l):
#            #print cpdist[l,fname].prob(fval)
#            return cpdist[l,fname].prob(fval)
#        labels = sorted([l for l in CLASSIFIER._labels
#                  if fval in cpdist[l,fname].samples()],
#                   key=labelprob) 
#       if len(labels) == 1: continue
#        l0 = labels[0]
#        l1 = labels[-1]
#        if cpdist[l0,fname].prob(fval) == 0:
#            ratio = 'INF'
#        else:
#            ratio = '%8.1f' % (cpdist[l1,fname].prob(fval) /
#                                 cpdist[l0,fname].prob(fval))
       # print ('%24s = %-14r %6s : %-6s = %s : 1.0' % 
        #              (fname, fval, str(l1)[:6], str(l0)[:6], ratio))

print CLASSIFIER.most_informative_features(100)
#CLASSIFIER = nltk.classify.maxent.train_maxent_CLASSIFIER_with_gis(v_train);



## classify and dump results for interpretation
#print "GOING TO PRINT ACCURACY"
#print '\nAccuracy %f\n' % nltk.classify.accuracy(CLASSIFIER, v_test)
#print CLASSIFIER.show_most_informative_features(200)




