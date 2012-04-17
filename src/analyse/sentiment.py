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
import tweet_features, tweet_pca
CORPUS1="../analyse/sentiment.csv"
CORPUS2="../analyse/newcorpus3"


    
def word_true_dict(words):
    feat={}
    for word in words:
        feat[word]=True
    return feat

def get_words_list(sentence, words_in_feature=4):
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
    num_words = 2
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
    
    #classification = CLASSIFIER.classify(tweet_features.make_tweet_dict(sentence))
    classification = CLASSIFIER.classify(word_true_dict(get_words_list(sentence)))
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
print fvecs[1]


#dump tweets which our feature selector found nothing
#for i in range(0,len(tweets)):
    #if tweet_features.is_zero_dict( fvecs[i][0] ):
        #print tweets[i][1] + ': ' + tweets[i][0]


## apply PCA reduction
# (v_train, v_test) = tweet_pca.tweet_pca_reduce( v_train, v_test, output_dim=1.0 )


## train CLASSIFIER

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


