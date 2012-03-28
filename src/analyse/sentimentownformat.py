"""
@package sentiment
Twitter sentiment analysis.

This code performs sentiment analysis on Tweets.

A custom feature extractor looks for key words and emoticons.  These are fed in
to a naive Bayes CLASSIFIER to assign a label of 'positive', 'negative', or
'neutral'.  Optionally, a principle components transform (PCT) is used to lessen
the influence of covariant features.

"""

import csv, random
import nltk
import ast
import tweet_features, tweet_pca
from keywords import extract_keywords
CORPUS1="../analyse/sentiment.csv"
CORPUS2="../analyse/corpusnew"

def analyse_sentiment(sentence):
    '''Analyses sentence sentiment. Returns a number of size
    representing sentiment with negative numbers meaning negative
    sentiment.'''
    global CLASSIFIER
    
    classification = CLASSIFIER.classify(tweet_features.make_tweet_dict(sentence))
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
with open(CORPUS1, 'rb') as fp:
    reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
    for row in reader:
        tweets.append([row[4], row[1]])

    
## treat neutral and irrelevant the same
for t in tweets:
    if t[1] == 'irrelevant':
        t[1] = 'neutral'
        
## split in to training and test sets
#print "SHUFFLING TWEETS"
random.shuffle(tweets);
#print "PUTTING INTO TRAINING AND TESTING VECTORS"
fvecs = [(tweet_features.make_tweet_dict(t),s) for (t,s) in tweets]
v_train = fvecs
#v_test  = fvecs[2000:]
#print v_test[450]


#dump tweets which our feature selector found nothing
#for i in range(0,len(tweets)):
#     if tweet_features.is_zero_dict( fvecs[i][0] ):
#         print tweets[i][1] + ': ' + tweets[i][0]


## apply PCA reduction
# (v_train, v_test) = tweet_pca.tweet_pca_reduce( v_train, v_test, output_dim=1.0 )


## train CLASSIFIER
#print "TRAINING NAIVESBAYESCLASSIFIER"
CLASSIFIER = nltk.NaiveBayesClassifier.train(v_train);
#CLASSIFIER = nltk.classify.maxent.train_maxent_CLASSIFIER_with_gis(v_train);

## classify and dump results for interpretation
#print "GOING TO PRINT ACCURACY"
#print '\nAccuracy %f\n' % nltk.classify.accuracy(CLASSIFIER, v_test)
print CLASSIFIER.show_most_informative_features(200)


# build confusion matrix over test set
#test_truth   = [s for (t,s) in v_test]
#test_predict = [CLASSIFIER.classify(t) for (t,s) in v_test]

#print 'Confusion Matrix'
#print nltk.ConfusionMatrix( test_truth, test_predict )


