'''Taken from http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/
 Basic machinelearning using NaiveBayesClassifier in nltk 
 and nltk corpus for movie reviews
 
'''
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
 
def word_feats(words):
    return dict([(word, True) for word in words])

def analyse(self,tweet):
    '''method that returns if a word is positive or negative'''
    return self.classifier.classify(word_feats(tweet))
    
def analyse_value(self,tweet):
    '''method that returns a value of how positive or negative a sentence is'''
    value=0
    itr=self.classifier
    for item in itr:
        value=value+item[1]
    return value
    
def test(self,tweet):
    value=0
    itr=self.classifier.probdist(word_feats(tweet)).items()
    for item in itr:
        value=value+item[1]
    return value
class MovieReviewBayes:
    '''Simple analys script found on the internet, trained on moviereviews'''
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
    #classifier._feature_probdist.items()[0].prob()
    cpdist = classifier._feature_probdist

    print classifier.most_informative_features(100)
    cpdist.get
    #print classifier.batch_prob_classify(word_feats("HAHA I DONT THINK THIS WILL WORK")).items()
  
analyser=MovieReviewBayes()

print analyse(analyser,"I DONT LIKE THIS CAR")
#test(analyser,"I DONT LIKE THIS CAR")

    
        


  