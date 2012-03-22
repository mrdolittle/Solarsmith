'''Taken from http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/
 Basic machinelearning using NaiveBayesClassifier in nltk 
 and nltk corpus for movie reviews
 
'''
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
 
def word_feats(words):
    return dict([(word, True) for word in words])
class MovieReviewBayes:
    '''Enkel analysmetod hittad på nätet på filmrecensioner'''
    
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
    
     
    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
    
        
    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4
     
    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    #print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
    #print  testfeats[450]
    classifier = NaiveBayesClassifier.train(trainfeats)
    #print 'accuracy:', nltk.classifMyClassy.util.accuracy(classifier, testfeats)
    classifier.show_most_informative_features()
    classifier.probdist(word_feats("I DONT LIKE CARS HAHA :)"))
    
    
    def analyse(self,tweet):
        '''Public method used for analysing tweet.'''
        
        return MovieReviewBayes.classifier.classify(word_feats(tweet))
    
    def analyse_value(self,tweet):
        '''Returns an arbitrary method to measure positive/negative.'''
        
        return MovieReviewBayes.classifier.prob_classify(word_feats(tweet)).items()
        
        

  
